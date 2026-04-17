"""
Module de traitement NLP pour extraction d'entites et classification
"""

import spacy
import pandas as pd
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NLPProcessor:
    """
    Processeur NLP pour analyse de contenu OSINT
    """
    
    def __init__(self, model_name: str = 'xx_ent_wiki_sm'):
        logger.info(f"Chargement modele spaCy: {model_name}")
        self.nlp = spacy.load(model_name)
        
        # Labels d'entites pertinents pour la securite
        self.relevant_entities = ['GPE', 'LOC', 'ORG', 'EVENT', 'NORP']
    
    def extract_entities(self, text: str) -> List[Dict]:
        """
        Extraction des entites nommees (lieux, organisations, etc.)
        
        Args:
            text: Texte a analyser
            
        Returns:
            Liste des entites trouvees
        """
        doc = self.nlp(text)
        entities = []
        
        for ent in doc.ents:
            if ent.label_ in self.relevant_entities:
                entities.append({
                    'text': ent.text,
                    'label': ent.label_,
                    'start': ent.start_char,
                    'end': ent.end_char
                })
        
        return entities
    
    def classify_severity(self, text: str) -> Dict:
        """
        Classification simple de la gravite basee sur mots-cles
        (A remplacer par modele Transformers en production)
        
        Args:
            text: Contenu a classifier
            
        Returns:
            Score et label de gravite
        """
        high_severity_words = [
            'attack', 'bombing', 'killed', 'injured', 'casualties',
            'explosion', 'shooting', 'hostage', 'massacre', 'dead'
        ]
        
        medium_severity_words = [
            'clash', 'protest', 'demonstration', 'blocked', 'checkpoint',
            'curfew', 'tension', 'threat', 'warning', 'danger'
        ]
        
        text_lower = text.lower()
        
        high_count = sum(1 for word in high_severity_words if word in text_lower)
        medium_count = sum(1 for word in medium_severity_words if word in text_lower)
        
        if high_count > 0:
            return {'score': min(0.8 + (high_count * 0.05), 1.0), 'label': 'HIGH'}
        elif medium_count > 0:
            return {'score': min(0.5 + (medium_count * 0.05), 0.79), 'label': 'MEDIUM'}
        else:
            return {'score': 0.2, 'label': 'LOW'}
    
    def process_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Traitement complet d'un DataFrame de tweets
        
        Args:
            df: DataFrame avec colonne 'content'
            
        Returns:
            DataFrame enrichi avec entites et gravite
        """
        logger.info(f"Traitement NLP de {len(df)} documents")
        
        # Extraction entites
        df['entities'] = df['content'].apply(self.extract_entities)
        
        # Classification gravite
        severity_results = df['content'].apply(self.classify_severity)
        df['severity_score'] = severity_results.apply(lambda x: x['score'])
        df['severity_label'] = severity_results.apply(lambda x: x['label'])
        
        # Extraction lieux uniques pour geocodage
        df['locations'] = df['entities'].apply(
            lambda ents: [e['text'] for e in ents if e['label'] in ['GPE', 'LOC']]
        )
        
        logger.info(f"Distribution gravite: {df['severity_label'].value_counts().to_dict()}")
        
        return df


if __name__ == "__main__":
    # Test
    processor = NLPProcessor()
    test_text = "Heavy clashes reported in Damascus suburb. Multiple casualties."
    print("Entites:", processor.extract_entities(test_text))
    print("Gravite:", processor.classify_severity(test_text))
