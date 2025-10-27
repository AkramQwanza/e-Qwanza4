import { useState } from "react";
import Layout from "@/components/Layout";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useToast } from "@/hooks/use-toast";
import { Download, Upload, FileText, CheckCircle } from "lucide-react";

const MaturityEvaluation = () => {
  const { toast } = useToast();
  const [isUploading, setIsUploading] = useState(false);

  const handleDownloadTemplate = () => {
    // Créer un lien de téléchargement vers le fichier Excel
    const link = document.createElement('a');
    link.href = '/Evaluation maturité DevSecOps 16 axes.xlsx';
    link.download = 'Evaluation maturité DevSecOps 16 axes.xlsx';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    toast({
      title: "Téléchargement",
      description: "Le questionnaire Excel est en cours de téléchargement.",
    });
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    // Vérifier que c'est un fichier Excel
    const allowedTypes = [
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', // .xlsx
      'application/vnd.ms-excel' // .xls
    ];
    
    if (!allowedTypes.includes(file.type)) {
      toast({
        title: "Erreur",
        description: "Veuillez sélectionner un fichier Excel (.xlsx ou .xls)",
        variant: "destructive",
      });
      return;
    }

    setIsUploading(true);
    
    try {
      // TODO: Implémenter l'upload du fichier vers le backend
      // Simuler un upload
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      toast({
        title: "Succès",
        description: "Le fichier Excel a été chargé avec succès. L'évaluation sera traitée.",
      });
      
      // Reset du input
      event.target.value = '';
      
    } catch (error) {
      toast({
        title: "Erreur",
        description: "Une erreur est survenue lors du chargement du fichier.",
        variant: "destructive",
      });
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <Layout className="h-screen">
      <div className="p-6 space-y-6">
        {/* Header */}
        <div className="text-center space-y-4">
          <h1 className="text-3xl font-bold text-foreground">
            Évaluation de maturité de votre SI
          </h1>
          <p className="text-lg text-muted-foreground max-w-3xl mx-auto">
            Afin d'évaluer la maturité de votre système d'information, veuillez suivre les étapes ci-dessous.
          </p>
        </div>

        {/* Steps */}
        <div className="grid md:grid-cols-2 gap-6 max-w-4xl mx-auto">
          {/* Step 1: Download Template */}
          <Card className="border-2 border-dashed border-primary/20 hover:border-primary/40 transition-colors">
            <CardHeader className="text-center">
              <div className="mx-auto w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mb-4">
                <FileText className="w-6 h-6 text-primary" />
              </div>
              <CardTitle className="text-xl">Étape 1</CardTitle>
              <CardDescription className="text-base">
                Téléchargez le questionnaire Excel et complétez-le avec vos réponses
              </CardDescription>
            </CardHeader>
            <CardContent className="text-center space-y-4">
              <p className="text-sm text-muted-foreground">
                Le questionnaire contient toutes les questions nécessaires pour évaluer la maturité de votre système d'information.
              </p>
              <Button 
                onClick={handleDownloadTemplate}
                className="w-full"
                size="lg"
              >
                <Download className="w-4 h-4 mr-2" />
                Télécharger le questionnaire Excel
              </Button>
            </CardContent>
          </Card>

          {/* Step 2: Upload Completed File */}
          <Card className="border-2 border-dashed border-primary/20 hover:border-primary/40 transition-colors">
            <CardHeader className="text-center">
              <div className="mx-auto w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mb-4">
                <Upload className="w-6 h-6 text-primary" />
              </div>
              <CardTitle className="text-xl">Étape 2</CardTitle>
              <CardDescription className="text-base">
                Chargez le fichier Excel complété pour traitement
              </CardDescription>
            </CardHeader>
            <CardContent className="text-center space-y-4">
              <p className="text-sm text-muted-foreground">
                Une fois le questionnaire complété, chargez-le ici pour générer votre rapport d'évaluation.
              </p>
              <div className="space-y-2">
                <input
                  type="file"
                  accept=".xlsx,.xls"
                  onChange={handleFileUpload}
                  disabled={isUploading}
                  className="hidden"
                  id="excel-upload"
                />
                <Button 
                  asChild
                  className="w-full"
                  size="lg"
                  disabled={isUploading}
                >
                  <label htmlFor="excel-upload" className="cursor-pointer">
                    <Upload className="w-4 h-4 mr-2" />
                    {isUploading ? "Chargement..." : "Charger le fichier Excel"}
                  </label>
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Instructions */}
        <Card className="max-w-4xl mx-auto">
          <CardHeader>
            <CardTitle className="flex items-center">
              <CheckCircle className="w-5 h-5 mr-2 text-green-500" />
              Instructions
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="space-y-2">
              <h4 className="font-semibold">1. Téléchargement du questionnaire :</h4>
              <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground ml-4">
                <li>Cliquez sur "Télécharger le questionnaire Excel"</li>
                <li>Le fichier sera téléchargé automatiquement</li>
                <li>Ouvrez le fichier avec Microsoft Excel ou LibreOffice Calc</li>
              </ul>
            </div>
            <div className="space-y-2">
              <h4 className="font-semibold">2. Complétion du questionnaire :</h4>
              <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground ml-4">
                <li>Répondez à toutes les questions dans les cellules prévues, en indiquant la bonne réponse.</li>
                <li>Un score sera attribué à chaque axe.</li>
                <li>Sauvegardez le fichier une fois terminé</li>
              </ul>
            </div>
            <div className="space-y-2">
              <h4 className="font-semibold">3. Chargement du fichier :</h4>
              <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground ml-4">
                <li>Cliquez sur "Charger le fichier Excel"</li>
                <li>Sélectionnez le fichier complété</li>
                <li>Attendez le traitement et la génération du rapport</li>
              </ul>
            </div>
          </CardContent>
        </Card>

        {/* Status */}
        <div className="text-center">
          <p className="text-sm text-muted-foreground">
            Une fois le fichier chargé, vous recevrez un rapport détaillé de l'évaluation de maturité de votre SI.
          </p>
        </div>
      </div>
    </Layout>
  );
};

export default MaturityEvaluation;
