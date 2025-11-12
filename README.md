# e-Qwanza - Manuel d'Installation

## 📋 Table des matières

1. [Prérequis système](#prérequis-système)
2. [Installation des outils de base](#installation-des-outils-de-base)
3. [Installation du Backend](#installation-du-backend)
4. [Installation du Frontend](#installation-du-frontend)
5. [Configuration des bases de données](#configuration-des-bases-de-données)
6. [Configuration des variables d'environnement](#configuration-des-variables-denvironnement)
7. [Démarrage de l'application](#démarrage-de-lapplication)
8. [Vérification de l'installation](#vérification-de-linstallation)

---

## 🔧 Prérequis système

Avant de commencer, assurez-vous d'avoir installé les outils suivants sur votre système :

### Outils requis

- **Python 3.11.0** ou supérieur ([Télécharger Python](https://www.python.org/downloads/))
- **Node.js 18.x** ou supérieur ([Télécharger Node.js](https://nodejs.org/))
- **npm** (inclus avec Node.js) ou **yarn**
- **Git** ([Télécharger Git](https://git-scm.com/downloads))
- **Docker Desktop** ([Télécharger Docker](https://www.docker.com/products/docker-desktop/)) - Optionnel mais recommandé pour les bases de données

### Vérification des installations

Ouvrez un terminal (PowerShell sur Windows, Terminal sur Mac/Linux) et vérifiez que tout est installé :

```bash
python --version    # Doit afficher Python 3.11.0 ou supérieur
node --version      # Doit afficher v18.x.x ou supérieur
npm --version       # Doit afficher une version npm
git --version       # Doit afficher une version git
docker --version    # Doit afficher une version docker (si installé)
```

---

## 📥 Installation des outils de base

### 1. Installation de Python 3.11.0

1. Téléchargez Python 3.11.0 depuis [python.org](https://www.python.org/downloads/)
2. **Important** : Lors de l'installation, cochez la case **"Add Python to PATH"**
3. Vérifiez l'installation : `python --version`

### 2. Installation de Node.js

1. Téléchargez Node.js 18.x LTS depuis [nodejs.org](https://nodejs.org/)
2. Installez Node.js (npm sera installé automatiquement)
3. Vérifiez l'installation : `node --version` et `npm --version`

### 3. Installation de Docker Desktop (Recommandé)

1. Téléchargez Docker Desktop depuis [docker.com](https://www.docker.com/products/docker-desktop/)
2. Installez et démarrez Docker Desktop
3. Vérifiez que Docker fonctionne : `docker --version`

---

## 🚀 Installation du Backend

### 1. Cloner le projet

Ouvrez un terminal et naviguez vers le répertoire où vous souhaitez installer le projet :

```bash
# Sur Windows (PowerShell)
cd Desktop
git clone https://github.com/AkramQwanza/e-Qwanza4.git
cd e-Qwanza4
```

### 2. Créer un environnement virtuel Python

```bash
# Naviguer vers le dossier backend
cd backend\src

# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement virtuel

# Sur Windows (CMD)
venv\Scripts\activate

# Sur Mac/Linux
source venv/bin/activate
```

**Note** : Si vous obtenez une erreur d'exécution de script sur PowerShell, exécutez d'abord :
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Installer les dépendances Python

Une fois l'environnement virtuel activé (vous devriez voir `(venv)` dans votre terminal) :

```bash
# Naviguer vers le dossier src
cd src

# Installer les dépendances
pip install --upgrade pip
pip install -r requirements.txt
```

**Note** : L'installation peut prendre plusieurs minutes, notamment pour les packages `torch` et `transformers` qui sont volumineux.

### 4. Installer les dépendances système (si nécessaire)

Certaines bibliothèques Python nécessitent des dépendances système :

#### Sur Windows
- Aucune dépendance système supplémentaire généralement requise

#### Sur Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install -y build-essential python3-dev libpq-dev
```

#### Sur Mac
```bash
brew install postgresql
```

---

## 🎨 Installation du Frontend

### 1. Naviguer vers le dossier frontend

Ouvrez un **nouveau terminal** (gardez le terminal du backend ouvert) :

```bash
# Depuis la racine du projet
cd frontend
```

### 2. Installer les dépendances Node.js

```bash
# Installer toutes les dépendances
npm install

# Ou si vous utilisez yarn
yarn install
```

**Note** : L'installation peut prendre quelques minutes.

---

## 🗄️ Configuration des bases de données

Le projet utilise **deux bases de données** :

1. **PostgreSQL avec pgvector** : Base de données principale pour stocker les données de l'application (utilisateurs, projets, conversations, etc.)
2. **Qdrant** : Base de données vectorielle pour stocker et rechercher les embeddings des documents

### Option 1 : Utiliser Docker (Recommandé)

C'est la méthode la plus simple pour démarrer les deux bases de données :

```bash
# Depuis la racine du projet
cd backend/docker

# Démarrer les conteneurs Docker (PostgreSQL et Qdrant)
docker-compose up -d

# Vérifier que les conteneurs sont en cours d'exécution
docker ps
```

Les bases de données seront accessibles sur :
- **PostgreSQL** : `localhost:5432`
- **Qdrant** : `http://localhost:6333` (API REST) et `http://localhost:6334` (gRPC)
- **Qdrant Dashboard** : `http://localhost:6333/dashboard` (interface web)

### Option 2 : Installation manuelle

#### PostgreSQL avec pgvector

1. Téléchargez PostgreSQL depuis [postgresql.org](https://www.postgresql.org/download/)
2. Installez PostgreSQL
3. Installez l'extension pgvector :
   ```bash
   # Sur Linux
   sudo apt-get install postgresql-17-pgvector
   
   # Sur Mac
   brew install pgvector
   ```
4. Créez une base de données et activez l'extension :
   ```sql
   CREATE DATABASE votre_base_de_donnees;
   \c votre_base_de_donnees
   CREATE EXTENSION vector;
   ```

#### Qdrant

1. **Option A : Installation via Docker** (recommandé)
   ```bash
   docker run -p 6333:6333 -p 6334:6334 -v $(pwd)/qdrant_storage:/qdrant/storage qdrant/qdrant
   ```

2. **Option B : Installation binaire**
   - Téléchargez Qdrant depuis [qdrant.tech](https://qdrant.tech/documentation/guides/installation/)
   - Suivez les instructions d'installation pour votre système d'exploitation

3. **Option C : Mode local (fichiers)**
   - Qdrant peut aussi fonctionner en mode local sans serveur
   - Dans ce cas, configurez `VECTOR_DB_PATH` dans le fichier `.env` pour pointer vers un dossier local

---

## ⚙️ Configuration des variables d'environnement

### 1. Créer le fichier .env pour le backend

Créez un fichier `.env` dans le dossier `backend/src/` :

```bash
# Depuis la racine du projet
cd backend/src
```

Créez le fichier `.env` avec le contenu suivant (adaptez les valeurs selon votre configuration) :

```env
# Configuration de l'application
APP_NAME=e-Qwanza
APP_VERSION=1.0.0

# Configuration des fichiers
FILE_ALLOWED_TYPES=["pdf","docx","pptx","txt","xlsx"]
FILE_MAX_SIZE=10485760
FILE_DEFAULT_CHUNK_SIZE=1000

# Configuration PostgreSQL
POSTGRES_USERNAME=postgres
POSTGRES_PASSWORD=votre_mot_de_passe_postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_MAIN_DATABASE=eqwanza_db

# Configuration des modèles LLM
GENERATION_BACKEND=openai
EMBEDDING_BACKEND=openai

# Clés API (remplacez par vos vraies clés)
OPENAI_API_KEY=votre_cle_api_openai
OPENAI_API_URL=https://api.openai.com/v1

# Ou si vous utilisez Cohere
# GENERATION_BACKEND=cohere
# EMBEDDING_BACKEND=cohere
# COHERE_API_KEY=votre_cle_api_cohere

# Configuration des modèles
GENERATION_MODEL_ID=gpt-4
EMBEDDING_MODEL_ID=text-embedding-3-small
EMBEDDING_MODEL_SIZE=1536

# Pour Cohere, utilisez :
# GENERATION_MODEL_ID=command-r
# EMBEDDING_MODEL_ID=embed-english-v3.0
# EMBEDDING_MODEL_SIZE=1024

# Configuration de la base de données vectorielle
# Choisissez entre "QDRANT" ou "PGVECTOR"
VECTOR_DB_BACKEND=QDRANT

# Si vous utilisez Qdrant en mode local (fichiers)
VECTOR_DB_PATH=./assets/database/qdrant_db

# Si vous utilisez Qdrant via Docker, vous devrez modifier le code pour utiliser l'URL
# VECTOR_DB_PATH=http://localhost:6333

# Si vous utilisez pgvector, cette variable n'est pas utilisée
VECTOR_DB_DISTANCE_METHOD=cosine
VECTOR_DB_PGVEC_INDEX_THRESHOLD=100

# Configuration de la langue
PRIMARY_LANG=fr
DEFAULT_LANG=fr

# Configuration JWT
JWT_SECRET_KEY=votre_secret_key_jwt_tres_securise
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=900
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Configuration des tokens (optionnel)
INPUT_DAFAULT_MAX_CHARACTERS=4000
GENERATION_DAFAULT_MAX_TOKENS=2000
GENERATION_DAFAULT_TEMPERATURE=0.7
```

### 2. Créer le fichier .env pour le frontend (optionnel)

Si vous devez changer l'URL de l'API backend, créez un fichier `.env` dans le dossier `frontend/` :

```env
VITE_API_BASE_URL=http://localhost:8000
```

---

## 🚀 Démarrage de l'application

### 1. Démarrer les bases de données (si vous utilisez Docker)

```bash
# Depuis backend/docker
cd backend/docker
docker-compose up -d
```

**Important** : Par défaut, le code utilise Qdrant en mode local (fichiers). Pour utiliser Qdrant via Docker, vous devez modifier le fichier `backend/src/stores/vectordb/providers/QdrantDBProvider.py` :

```python
# Ligne 26, remplacer :
self.client = QdrantClient(path=self.db_client)

# Par :
self.client = QdrantClient(url="http://localhost:6333")
```

Ou configurez `VECTOR_DB_PATH=http://localhost:6333` dans votre fichier `.env` et modifiez le code pour détecter si c'est une URL ou un chemin.

### 2. Démarrer le backend

Ouvrez un terminal et :

```bash
# Naviguer vers backend/src
cd backend/src

# Activer l'environnement virtuel (si pas déjà fait)
# Sur Windows (PowerShell)
..\venv\Scripts\Activate.ps1

# Sur Mac/Linux
source ../venv/bin/activate

# Démarrer le serveur FastAPI
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Le backend sera accessible sur : `http://localhost:8000`
- Documentation API : `http://localhost:8000/docs`
- Documentation alternative : `http://localhost:8000/redoc`

### 3. Démarrer le frontend

Ouvrez un **nouveau terminal** et :

```bash
# Naviguer vers frontend
cd frontend

# Démarrer le serveur de développement
npm run dev

# Ou avec yarn
yarn dev
```

Le frontend sera accessible sur : `http://localhost:8080`

---

## ✅ Vérification de l'installation

### Vérifier le backend

1. Ouvrez votre navigateur et allez sur `http://localhost:8000/docs`
2. Vous devriez voir la documentation interactive de l'API FastAPI
3. Testez l'endpoint de santé : `http://localhost:8000/health` (si disponible)

### Vérifier le frontend

1. Ouvrez votre navigateur et allez sur `http://localhost:8080`
2. Vous devriez voir l'interface de l'application
3. Vérifiez que la connexion au backend fonctionne

### Vérifier les bases de données

#### PostgreSQL
```bash
# Si vous utilisez Docker
docker exec -it pgvector psql -U postgres -d eqwanza_db

# Ou avec PostgreSQL installé localement
psql -U postgres -d eqwanza_db
```

#### Qdrant
```bash
# Si vous utilisez Docker, vérifiez que le conteneur est en cours d'exécution
docker ps | grep qdrant

# Accédez au dashboard Qdrant dans votre navigateur
# http://localhost:6333/dashboard

# Ou testez l'API REST
curl http://localhost:6333/collections
```

**Note** : Si vous utilisez Qdrant en mode local (fichiers), vérifiez que le dossier `VECTOR_DB_PATH` existe et est accessible.

---

## 🔍 Dépannage

### Problèmes courants

#### 1. Erreur "Python not found"
- Vérifiez que Python est installé : `python --version`
- Vérifiez que Python est dans le PATH
- Sur Windows, réinstallez Python en cochant "Add Python to PATH"

#### 2. Erreur lors de l'installation de `torch` ou `transformers`
- Ces packages sont volumineux, attendez la fin du téléchargement
- Si l'erreur persiste, installez-les séparément :
  ```bash
  pip install torch --index-url https://download.pytorch.org/whl/cpu
  pip install transformers
  ```

#### 3. Erreur de connexion à la base de données PostgreSQL
- Vérifiez que Docker est démarré : `docker ps`
- Vérifiez que le conteneur PostgreSQL est en cours d'exécution : `docker ps | grep pgvector`
- Vérifiez les identifiants dans le fichier `.env`
- Testez la connexion : `docker exec -it pgvector psql -U postgres -d eqwanza_db`

#### 3b. Erreur de connexion à Qdrant
- Vérifiez que le conteneur Qdrant est en cours d'exécution : `docker ps | grep qdrant`
- Vérifiez que Qdrant est accessible : `curl http://localhost:6333/collections`
- Si vous utilisez Qdrant en mode local, vérifiez que le dossier `VECTOR_DB_PATH` existe
- Si vous utilisez Qdrant via Docker, assurez-vous d'avoir modifié le code pour utiliser l'URL (voir section "Démarrage de l'application")

#### 4. Erreur "Module not found"
- Vérifiez que l'environnement virtuel est activé
- Réinstallez les dépendances : `pip install -r requirements.txt`

#### 5. Erreur CORS dans le navigateur
- Vérifiez que le backend est démarré sur le port 8000
- Vérifiez la configuration CORS dans `main.py`

#### 6. Erreur "Port already in use"
- Arrêtez le processus utilisant le port :
  ```bash
  # Sur Windows
  netstat -ano | findstr :8000
  taskkill /PID <PID> /F
  
  # Sur Mac/Linux
  lsof -ti:8000 | xargs kill
  ```

---

## 📚 Ressources supplémentaires

- [Documentation FastAPI](https://fastapi.tiangolo.com/)
- [Documentation React](https://react.dev/)
- [Documentation Docker](https://docs.docker.com/)
- [Documentation PostgreSQL](https://www.postgresql.org/docs/)
- [Documentation MongoDB](https://www.mongodb.com/docs/)

---

## 📝 Notes importantes

1. **Sécurité** : Ne commitez jamais le fichier `.env` contenant vos clés API dans Git
2. **Environnement virtuel** : N'oubliez pas d'activer l'environnement virtuel avant de travailler sur le backend
3. **Ports** : Assurez-vous que les ports suivants sont disponibles :
   - `8000` : Backend FastAPI
   - `8080` : Frontend React
   - `5432` : PostgreSQL
   - `6333` : Qdrant API REST
   - `6334` : Qdrant gRPC
4. **Clés API** : Vous devez obtenir vos propres clés API depuis :
   - OpenAI : [platform.openai.com](https://platform.openai.com/api-keys)
   - Cohere : [dashboard.cohere.com](https://dashboard.cohere.com/)

---

## 🆘 Support

Si vous rencontrez des problèmes lors de l'installation, vérifiez :
1. Que tous les prérequis sont installés
2. Que toutes les dépendances sont installées
3. Que les bases de données sont démarrées
4. Que le fichier `.env` est correctement configuré

Pour plus d'aide, consultez la documentation du projet ou ouvrez une issue sur GitHub.
