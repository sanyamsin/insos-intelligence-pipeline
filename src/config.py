"""
Configuration centralisee du pipeline OSINT
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Base de donnees PostgreSQL - VOTRE MOT DE PASSE
POSTGRES_CONFIG = {
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'port': os.getenv('POSTGRES_PORT', '5432'),
    'database': os.getenv('POSTGRES_DB', 'postgres'),
    'user': os.getenv('POSTGRES_USER', 'postgres'),
    'password': os.getenv('POSTGRES_PASSWORD', 'Test')
}

# Elasticsearch
ELASTICSEARCH_CONFIG = {
    'host': os.getenv('ES_HOST', 'localhost'),
    'port': os.getenv('ES_PORT', '9200')
}

# Collecte
COLLECTION_CONFIG = {
    'max_tweets_per_run': 1000,
    'keywords': ['Ukraine', 'Syria', 'conflict', 'security', 'attack'],
    'geofence': {
        'lat_min': 44.0,
        'lat_max': 53.0,
        'lon_min': 22.0,
        'lon_max': 40.0
    }
}

# NLP
NLP_CONFIG = {
    'spacy_model': 'xx_ent_wiki_sm',
    'severity_threshold': 0.7
}
