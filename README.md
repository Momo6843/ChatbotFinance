# 🤖 Assistant Stratégique IA - ChatbotFinance

Un assistant IA intelligent pour l'analyse de documents PDF utilisant la technologie RAG (Retrieval Augmented Generation) avec une interface intuitive.

## 📋 Vue d'ensemble

Ce projet combine une interface frontend conviviale (Streamlit) avec un backend robuste (FastAPI) pour créer un assistant IA capable de :
- 📄 Traiter et indexer des documents PDF
- 🔍 Rechercher des informations pertinentes dans les documents
- 💬 Générer des réponses intelligentes basées sur le contenu des documents
- 📊 Afficher un historique des questions posées
- 🏷️ Filtrer les résultats par PDF, pages et tags

## 🏗️ Architecture

```
chatbotFinance/
├── backend/               # Serveur FastAPI
│   ├── main.py           # Point d'entrée principale
│   ├── db/
│   │   ├── chroma.py     # Client ChromaDB (stockage vectoriel)
│   │   └── postgres.py   # Client PostgreSQL (métadonnées)
│   ├── routes/
│   │   ├── chat.py       # Endpoint chat
│   │   └── upload.py     # Endpoint upload
│   └── services/
│       ├── embeddings.py # Génération d'embeddings (Cohere)
│       ├── pdf_processor.py # Extraction et chunking de PDF
│       └── rag.py        # Logique RAG
├── frontend/              # Interface Streamlit
│   └── app.py            # Application web
├── chroma_db/            # Base de données ChromaDB
└── requirement.txt       # Dépendances Python
```

## 🚀 Installation

### Prérequis
- Python 3.8+
- PostgreSQL (version 12+)
- Clés API : Cohere

### Étapes d'installation

1. **Cloner ou extraire le projet**
```bash
cd chatbotFinance
```

2. **Créer un environnement virtuel** (optionnel mais recommandé)
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

3. **Installer les dépendances**
```bash
pip install -r requirement.txt
```

4. **Configurer les variables d'environnement**

Créez un fichier `.env` à la racine du projet :
```env
# Cohere
COHERE_API_KEY=votre_clé_cohere

# PostgreSQL
POSTGRES_USER=postgres
POSTGRES_PASSWORD=006750
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
POSTGRES_DB=ragfinance

# ChromaDB
CHROMA_DIR=./chroma_db
```

5. **Initialiser la base de données PostgreSQL**

Assurez-vous que PostgreSQL fonctionne sur le port 5433, puis créez la base de données :
```sql
CREATE DATABASE ragfinance;
```

## 📖 Utilisation

### Démarrer le backend
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### Démarrer le frontend
Dans un nouveau terminal :
```bash
cd frontend
streamlit run app.py
```

L'application sera accessible sur `http://localhost:8501`

## 💡 Fonctionnalités

### 📤 Upload de Documents
- Sélectionnez un PDF via l'interface
- Choisissez le type de document :
  - **Passager** : Indexation page par page
  - **Définitif** : Regroupement par chunks de 3 pages
- Ajoutez des tags pour faciliter le filtrage

### 💬 Chat avec l'Assistant
- Posez des questions sur vos documents
- Filtrez par :
  - Nom du PDF
  - Numéros de pages (ex: 2,3,4)
  - Tags (ex: finance, contrat)
- Obtenez des réponses avec sources

### 📊 Tableau de Bord
- Visualisez tous les documents stockés
- Consultez l'historique de vos questions
- Affichez le nombre de tags par document

## 🔧 Configuration Avancée

### Modifier le modèle IA
Dans [backend/services/rag.py](backend/services/rag.py#L23), changez le modèle Cohere :
```python
model="command-a-03-2025"  # Remplacer par un autre modèle
```

### Ajuster la taille des chunks
Dans [backend/services/pdf_processor.py](backend/services/pdf_processor.py#L11), modifiez `chunk_size` :
```python
def chunk_pages(pages, chunk_size=3):  # Augmentez ou diminuez cette valeur
```

### Nombre de résultats RAG
Dans [backend/services/rag.py](backend/services/rag.py#L10), changez `top_k` :
```python
def retrieve_context(question, pdf_filter=None, page_filter=None, tag_filter=None, top_k=5):
```

## 📦 Dépendances Principales

- **FastAPI** : Framework web haute performance
- **Streamlit** : Interface utilisateur interactive
- **ChromaDB** : Base de données vectorielle
- **PostgreSQL** : Stockage des métadonnées
- **Cohere** : Modèles d'IA (embeddings et génération)
- **pdfplumber** : Extraction de texte des PDFs

## 🔐 Sécurité

- ⚠️ **À proscrire en production** : Les identifiants PostgreSQL sont hardcodés
- Utilisez des variables d'environnement ou un gestionnaire de secrets
- Restreignez l'origine CORS si nécessaire dans `main.py`

## 🐛 Dépannage

### Erreur de connexion PostgreSQL
```
Vérifiez que PostgreSQL fonctionne sur le port 5433
Vérifiez les identifiants dans le fichier .env
```

### Erreur de clé API Cohere
```
Vérifiez que COHERE_API_KEY est définie dans le fichier .env
Vérifiez que votre clé API est valide
```

### Problème d'affichage Streamlit
```bash
# Effacez le cache
streamlit cache clear

# Redémarrez l'application
```

## 📝 Notes

- Les embeddings sont générés avec le modèle Cohere "small"
- Les réponses sont limitées à 300 tokens
- L'historique est stocké pendant 50 dernières questions

## 📧 Support

Pour toute question ou problème, consultez la documentation officielle :
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Cohere Documentation](https://docs.cohere.com/)

---

**Dernière mise à jour** : Janvier 2026
