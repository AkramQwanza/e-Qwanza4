import os
import tempfile
from typing import Dict, List, Any
from fastapi import UploadFile, HTTPException
from fastapi.responses import JSONResponse
from helpers.excel_parser import ExcelMaturityParser
from stores.llm.LLMProviderFactory import LLMProviderFactory
from helpers.config import get_settings

class MaturityController:
    def __init__(self):
        try:
            self.settings = get_settings()
            self.llm_factory = LLMProviderFactory()
        except Exception as e:
            print(f"ATTENTION: Configuration non disponible: {e}")
            self.settings = None
            self.llm_factory = None
    
    async def analyze_maturity_excel(self, file: UploadFile, eval_type: str | None = None) -> Dict[str, Any]:
        """Analyse le fichier Excel de maturité et génère des recommandations"""
        try:
            print(f"🔍 Début de l'analyse du fichier: {file.filename}")
            # Vérifier le type de fichier (Excel ou CSV)
            allowed_ext = ('.xlsx', '.xls', '.csv')
            if not file.filename.lower().endswith(allowed_ext):
                raise HTTPException(
                    status_code=400,
                    detail="Le fichier doit être au format .xlsx, .xls ou .csv"
                )
            
            # Sauvegarder temporairement le fichier
            suffix = '.csv' if file.filename.lower().endswith('.csv') else '.xlsx'
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
                content = await file.read()
                tmp_file.write(content)
                tmp_file_path = tmp_file.name
            
            try:
                # Parser le fichier Excel
                parser = ExcelMaturityParser(tmp_file_path)
                # Selon le besoin, on peut soit garder l'ancien modèle d'axes,
                # soit retourner un DataFrame normalisé depuis le CSV.
                axes = parser.parse()
                records = parser.parse_records()

                # Construire une table de correspondance axe -> score à partir de flat_records
                def _normalize_axis_label(label: str) -> str:
                    import re
                    base = label or ""
                    base = base.strip()
                    # Supprimer le préfixe "Axe X -" ou variantes
                    base = re.sub(r'(?i)^axe\s*\d+\s*[-–:]\s*', '', base).strip()
                    return base.lower()

                record_axis_score_map = {}
                for rec in records or []:
                    axe_label = rec.get("axe")
                    axe_score = rec.get("axe_score")
                    if axe_label and axe_score is not None:
                        key = _normalize_axis_label(axe_label)
                        # Premier score rencontré fait foi; on peut aussi écraser par le dernier, identique ici
                        record_axis_score_map[key] = axe_score
                
                if not axes:
                    raise HTTPException(
                        status_code=400,
                        detail="Aucun axe d'évaluation trouvé dans le fichier Excel"
                    )
                
                # Identifier les opportunités d'amélioration
                opportunities = parser.get_improvement_opportunities()
                
                # Générer des recommandations avec LLM
                recommendations = await self._generate_recommendations(opportunities)
                
                # Calculer le score global selon le type
                eval_type_norm = (eval_type or "devsecops").lower()
                if eval_type_norm == "architecture":
                    # Architecture: se baser sur les moyennes des axes détectés par le parseur
                    axis_scores = [axis.average_score for axis in axes if axis.average_score is not None]
                    global_score = round(sum(axis_scores) / len(axis_scores), 2) if axis_scores else 0.0
                else:
                    # DevSecOps (par défaut): prioriser les scores issus des flat_records, sinon fallback aux axes
                    scores = [s for s in record_axis_score_map.values() if s is not None]
                    if scores:
                        global_score = round(sum(scores) / len(scores), 2)
                    else:
                        global_score = self._calculate_global_score(axes)

                # Préparer la réponse
                response = {
                    "evaluation_type": eval_type_norm,
                    "global_score": global_score,
                    "total_axes": len(axes),
                    "axes_analysis": [
                        {
                            "name": axis.name,
                            "definition": axis.definition,
                            # Architecture: garder la moyenne de l'axe tel que parsée; DevSecOps: possibilité d'écraser via flat_records
                            "average_score": round(
                                (axis.average_score if eval_type_norm == "architecture" else (record_axis_score_map.get(_normalize_axis_label(axis.name), axis.average_score))) or 0.0,
                                2
                            ),
                            "max_score": 5.0,
                            "questions_count": len(axis.questions)
                        }
                        for axis in axes
                    ],
                    "flat_records": records,  # format tabulaire prêt pour le RAG
                    "improvement_opportunities": opportunities,
                    "recommendations": recommendations
                }
                
                return response
                
            finally:
                # Nettoyer le fichier temporaire
                if os.path.exists(tmp_file_path):
                    os.unlink(tmp_file_path)
                    
        except Exception as e:
            print(f"❌ Erreur dans analyze_maturity_excel: {str(e)}")
            print(f"❌ Type d'erreur: {type(e).__name__}")
            import traceback
            print(f"❌ Traceback: {traceback.format_exc()}")
            raise HTTPException(
                status_code=500,
                detail=f"Erreur lors de l'analyse du fichier: {str(e)}"
            )
    
    async def _generate_recommendations(self, opportunities: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Génère des recommandations avec LLM pour chaque opportunité"""
        recommendations = {
            "short_term": [],  # 0-3 mois
            "medium_term": [],  # 3-12 mois
            "long_term": []  # 12+ mois
        }
        
        # Initialiser le LLM
        if self.llm_factory is None:
            print("ATTENTION: LLM non disponible, utilisation de recommandations par défaut")
            return self._generate_default_recommendations(opportunities)
        
        llm_provider = self.llm_factory.get_provider("cohere")
        
        for opportunity in opportunities:
            # Créer le prompt pour le LLM
            prompt = self._create_recommendation_prompt(opportunity)
            
            try:
                # Générer les recommandations avec le LLM
                llm_response = await llm_provider.generate_response(
                    prompt=prompt,
                    max_tokens=1000,
                    temperature=0.7
                )
                
                # Parser la réponse du LLM
                parsed_recommendations = self._parse_llm_response(llm_response)
                
                # Organiser par échéance
                for rec in parsed_recommendations:
                    timeline = rec.get("timeline", "medium_term")
                    if timeline in recommendations:
                        recommendations[timeline].append({
                            "axis_name": opportunity["axis_name"],
                            "question": opportunity["question"],
                            "current_situation": opportunity["current_response"],
                            "target_situation": opportunity["next_level_response"],
                            "recommendation": rec["action"],
                            "timeline": rec["timeline"],
                            "priority": rec.get("priority", "medium")
                        })
                        
            except Exception as e:
                print(f"Erreur LLM pour l'axe {opportunity['axis_name']}: {str(e)}")
                # Ajouter une recommandation par défaut
                recommendations["medium_term"].append({
                    "axis_name": opportunity["axis_name"],
                    "question": opportunity["question"],
                    "current_situation": opportunity["current_response"],
                    "target_situation": opportunity["next_level_response"],
                    "recommendation": f"Améliorer {opportunity['axis_name']} en passant de '{opportunity['current_response'][:50]}...' à '{opportunity['next_level_response'][:50]}...'",
                    "timeline": "medium_term",
                    "priority": "medium"
                })
        
        return recommendations
    
    def _generate_default_recommendations(self, opportunities: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Génère des recommandations par défaut sans LLM"""
        recommendations = {
            "short_term": [],
            "medium_term": [],
            "long_term": []
        }
        
        for opportunity in opportunities:
            # Recommandation par défaut
            default_rec = {
                "axis_name": opportunity["axis_name"],
                "question": opportunity["question"],
                "current_situation": opportunity["current_response"],
                "target_situation": opportunity["next_level_response"],
                "recommendation": f"Améliorer {opportunity['axis_name']} en passant de '{opportunity['current_response'][:50]}...' à '{opportunity['next_level_response'][:50]}...'. Mettre en place un plan d'action progressif.",
                "timeline": "medium_term",
                "priority": "medium"
            }
            
            recommendations["medium_term"].append(default_rec)
        
        return recommendations
    
    def _create_recommendation_prompt(self, opportunity: Dict[str, Any]) -> str:
        """Crée le prompt pour le LLM"""
        return f"""
Dans le contexte d'un audit de maturité DevSecOps, analysez cette situation :

**Axe d'évaluation :** {opportunity['axis_name']}
**Définition de l'axe :** {opportunity['axis_definition']}

**Question :** {opportunity['question']}

**Situation actuelle :** {opportunity['current_response']} (Score: {opportunity['current_score']}/5)

**Objectif :** {opportunity['next_level_response']} (Score: {opportunity['next_level_score']}/5)

**Mission :** Fournir des recommandations concrètes et actionables pour permettre au client d'atteindre l'objectif au prochain audit.

Répondez au format JSON suivant :
{{
    "recommendations": [
        {{
            "action": "Action concrète à mettre en œuvre",
            "timeline": "short_term|medium_term|long_term",
            "priority": "high|medium|low",
            "description": "Explication détaillée de l'action"
        }}
    ]
}}

Considérez :
- Les contraintes techniques et organisationnelles
- Les dépendances entre les actions
- La faisabilité selon la taille de l'organisation
- Les bonnes pratiques DevSecOps
"""
    
    def _parse_llm_response(self, response: str) -> List[Dict[str, Any]]:
        """Parse la réponse du LLM"""
        try:
            import json
            # Essayer de parser le JSON
            data = json.loads(response)
            return data.get("recommendations", [])
        except:
            # Si le parsing JSON échoue, créer une recommandation par défaut
            return [{
                "action": "Analyser et améliorer les processus actuels",
                "timeline": "medium_term",
                "priority": "medium",
                "description": response[:200] + "..." if len(response) > 200 else response
            }]
    
    def _calculate_global_score(self, axes: List) -> float:
        """Calcule le score global de maturité"""
        if not axes:
            return 0.0
        for axis in axes:
            print(f"🔍 Calcul du score global: {axis.average_score}")

        print(axes)
        total_score = sum(axis.average_score for axis in axes)
        print(f"🔍 Calcul du score global:{total_score} ")
        return round(total_score / len(axes), 2)
