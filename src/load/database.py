"""
Module de persistance des donnees - POSTGRESQL
Compatible SQLAlchemy 2.0
"""

import psycopg2
from psycopg2.extras import execute_values
import pandas as pd
from sqlalchemy import create_engine, text
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SecurityDatabase:
    """
    Interface de stockage pour les alertes de securite
    """
    
    def __init__(self, host: str, port: str, database: str, user: str, password: str):
        self.connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        self.engine = create_engine(self.connection_string)
        self.init_tables()
    
    def init_tables(self):
        """Creation des tables si non existantes"""
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS security_alerts (
            id SERIAL PRIMARY KEY,
            source_id VARCHAR(255) UNIQUE,
            source_type VARCHAR(50),
            content TEXT,
            raw_entities JSONB,
            locations TEXT[],
            primary_location VARCHAR(255),
            latitude DECIMAL(10, 8),
            longitude DECIMAL(11, 8),
            country VARCHAR(100),
            severity_score DECIMAL(3, 2),
            severity_label VARCHAR(50),
            verification_status VARCHAR(20) DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            collected_at TIMESTAMP
        );
        
        CREATE INDEX IF NOT EXISTS idx_severity ON security_alerts(severity_label);
        
        CREATE INDEX IF NOT EXISTS idx_created ON security_alerts(created_at);
        """
        
        with self.engine.begin() as conn:
            conn.execute(text(create_table_sql))
        
        logger.info("Tables PostgreSQL initialisees")
    
    def insert_alerts(self, df: pd.DataFrame):
        """
        Insertion batch d'alertes
        
        Args:
            df: DataFrame traite par le pipeline
        """
        records = []
        for _, row in df.iterrows():
            # Convertir les listes en format PostgreSQL array
            locations = row.get('locations', [])
            if isinstance(locations, str):
                locations = json.loads(locations)
            
            # Format PostgreSQL array: {item1,item2}
            pg_locations = '{' + ','.join(locations) + '}' if locations else '{}'
            
            records.append((
                str(row.get('id', '')),
                row.get('source', 'unknown'),
                row.get('content', ''),
                row.get('entities', '[]'),  # JSONB accepte string JSON
                pg_locations,
                row.get('primary_location'),
                row.get('latitude'),
                row.get('longitude'),
                row.get('country', 'unknown'),
                row.get('severity_score', 0.0),
                row.get('severity_label', 'UNKNOWN'),
                row.get('date')
            ))
        
        insert_sql = """
        INSERT INTO security_alerts 
        (source_id, source_type, content, raw_entities, locations, 
         primary_location, latitude, longitude, country, severity_score, 
         severity_label, collected_at)
        VALUES %s
        ON CONFLICT (source_id) DO NOTHING
        """
        
        with psycopg2.connect(self.connection_string) as conn:
            with conn.cursor() as cur:
                execute_values(cur, insert_sql, records)
            conn.commit()
        
        logger.info(f"Inseres: {len(records)} alertes")
    
    def get_all_alerts(self) -> pd.DataFrame:
        """
        Recuperer toutes les alertes
        
        Returns:
            DataFrame des alertes
        """
        query = "SELECT * FROM security_alerts ORDER BY created_at DESC"
        return pd.read_sql(query, self.engine)
    
    def get_stats(self) -> dict:
        """
        Statistiques rapides
        
        Returns:
            Dictionnaire des stats
        """
        with self.engine.connect() as conn:
            total = conn.execute(text("SELECT COUNT(*) FROM security_alerts")).scalar()
            
            result = conn.execute(text("SELECT severity_label, COUNT(*) FROM security_alerts GROUP BY severity_label"))
            severity_counts = {row[0]: row[1] for row in result}
            
            return {
                'total_alerts': total,
                'by_severity': severity_counts
            }


if __name__ == "__main__":
    from src.config import POSTGRES_CONFIG
    db = SecurityDatabase(**POSTGRES_CONFIG)
    print("Connexion PostgreSQL OK")
    print("Stats:", db.get_stats())
