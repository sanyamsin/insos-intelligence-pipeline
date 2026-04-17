# 🛡️ OSINT Security Intelligence Pipeline

Pipeline de surveillance open-source pour la securite humanitaire. 
Concu pour les ONG operant en zones de crise.

## 🎯 Objectif

Collecter, traiter et visualiser des donnees open-source (reseaux sociaux, 
actualites) pour alerter les equipes humanitaires sur les risques de securite.

## 🏗️ Architecture

Sources OSINT (Twitter) → Orchestrateur Python → NLP (spaCy) → PostgreSQL → Dashboard Streamlit


## 🚀 Demarrage rapide

### Prerequis
- Python 3.12+
- PostgreSQL (avec mot de passe configure)

### Installation

`ash
# Cloner le repository
git clone https://github.com/sanyamsin/insos-intelligence-pipeline.git
cd insos-intelligence-pipeline

# Environnement virtuel
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Dependances
pip install -r requirements.txt

# Modele spaCy
python -m spacy download xx_ent_wiki_sm

# Configuration PostgreSQL
Modifier src/config.py avec vos credentials :
POSTGRES_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'database': 'postgres',
    'user': 'postgres',
    'password': 'VOTRE_MOT_DE_PASSE'
}

# Lancer le pipeline
# Une execution
python scripts/orchestrator.py --mode once

# Mode planifie (toutes les heures)
python scripts/orchestrator.py --mode scheduled

Lancer le dashboard
streamlit run src/dashboard/app.py
Acces : http://localhost:8501

Structure du projet 

| Dossier          | Contenu                      |
| ---------------- | ---------------------------- |
| src/extract/   | Collecte Twitter             |
| src/transform/ | NLP + Geocodage              |
| src/load/      | Persistance PostgreSQL       |
| src/dashboard/ | Visualisation Streamlit      |
| scripts/       | Orchestrateur + Donnees test |

🛠️ Stack technique
Python 3.12 - Langage principal
spaCy 3.7 - NLP et extraction d'entites
PostgreSQL - Base de donnees
Streamlit - Dashboard interactif
Plotly/Folium - Visualisations

🧪 Donnees de test
python scripts/generate_test_data.py

📈 Fonctionnalites
✅ Collecte Twitter via snscrape (sans API key)
✅ Extraction d'entites (lieux, organisations)
✅ Classification de gravite (HIGH/MEDIUM/LOW)
✅ Geocodage des lieux mentionnes
✅ Stockage PostgreSQL avec index geospatial
✅ Dashboard interactif avec cartes graphiques

📝 Auteur
Serge-Alain NYAMSIN - Data Scientist & Humanitaire
+12 ans d'experience ONG + Diplome DSTI Paris 2025
LinkedIn : linkedin.com/in/serge-alain-nyamsin

📄 Licence
MIT License
