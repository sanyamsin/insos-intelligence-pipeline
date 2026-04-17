"""
Script de generation de donnees de test pour le dashboard
"""

import sys
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.load.database import SecurityDatabase
from src.config import POSTGRES_CONFIG
import pandas as pd
from datetime import datetime, timedelta

# Donnees de test factices - LISTES PYTHON (pas JSON strings)
test_data = [
    {
        'id': 'tweet_001',
        'source': 'twitter',
        'content': 'Heavy clashes reported in Damascus suburb. Multiple casualties and injured civilians. #Syria',
        'entities': '[{\"text\": \"Damascus\", \"label\": \"GPE\"}, {\"text\": \"Syria\", \"label\": \"GPE\"}]',
        'locations': ['Damascus', 'Syria'],
        'primary_location': 'Damascus, Syria',
        'latitude': 33.5138,
        'longitude': 36.2765,
        'country': 'Syria',
        'severity_score': 0.85,
        'severity_label': 'HIGH',
        'date': datetime.now() - timedelta(hours=2)
    },
    {
        'id': 'tweet_002',
        'source': 'twitter',
        'content': 'Protest in Kyiv city center. Large crowd gathered near Maidan Nezalezhnosti. Tension rising.',
        'entities': '[{\"text\": \"Kyiv\", \"label\": \"GPE\"}, {\"text\": \"Maidan Nezalezhnosti\", \"label\": \"LOC\"}]',
        'locations': ['Kyiv', 'Ukraine'],
        'primary_location': 'Kyiv, Ukraine',
        'latitude': 50.4501,
        'longitude': 30.5234,
        'country': 'Ukraine',
        'severity_score': 0.55,
        'severity_label': 'MEDIUM',
        'date': datetime.now() - timedelta(hours=5)
    },
    {
        'id': 'tweet_003',
        'source': 'twitter',
        'content': 'Checkpoint established on highway near Aleppo. Traffic blocked in both directions.',
        'entities': '[{\"text\": \"Aleppo\", \"label\": \"GPE\"}]',
        'locations': ['Aleppo', 'Syria'],
        'primary_location': 'Aleppo, Syria',
        'latitude': 36.2021,
        'longitude': 37.1343,
        'country': 'Syria',
        'severity_score': 0.45,
        'severity_label': 'MEDIUM',
        'date': datetime.now() - timedelta(hours=8)
    },
    {
        'id': 'tweet_004',
        'source': 'twitter',
        'content': 'Explosion heard in Kharkiv residential area. Emergency services responding. Stay safe.',
        'entities': '[{\"text\": \"Kharkiv\", \"label\": \"GPE\"}]',
        'locations': ['Kharkiv', 'Ukraine'],
        'primary_location': 'Kharkiv, Ukraine',
        'latitude': 49.9935,
        'longitude': 36.2304,
        'country': 'Ukraine',
        'severity_score': 0.90,
        'severity_label': 'HIGH',
        'date': datetime.now() - timedelta(hours=12)
    },
    {
        'id': 'tweet_005',
        'source': 'twitter',
        'content': 'Curfew announced in Latakia starting 8 PM tonight. Residents advised to stay indoors.',
        'entities': '[{\"text\": \"Latakia\", \"label\": \"GPE\"}]',
        'locations': ['Latakia', 'Syria'],
        'primary_location': 'Latakia, Syria',
        'latitude': 35.5310,
        'longitude': 35.7915,
        'country': 'Syria',
        'severity_score': 0.35,
        'severity_label': 'LOW',
        'date': datetime.now() - timedelta(hours=24)
    }
]

if __name__ == "__main__":
    print("Insertion de donnees de test...")
    
    # Creer DataFrame
    df = pd.DataFrame(test_data)
    
    # Connexion base de donnees
    db = SecurityDatabase(**POSTGRES_CONFIG)
    
    # Inserer donnees
    db.insert_alerts(df)
    
    # Verifier
    stats = db.get_stats()
    print(f"Donnees inserees: {stats}")
    print("Done! Rafraichissez le dashboard Streamlit.")
