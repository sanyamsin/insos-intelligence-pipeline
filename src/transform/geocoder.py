"""
Module de geocodage pour enrichissement spatial
"""

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import pandas as pd
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GeoEnricher:
    """
    Enrichissement geospatial des alertes OSINT
    """
    
    def __init__(self, user_agent: str = 'insos-pipeline'):
        self.geolocator = Nominatim(user_agent=user_agent)
        self.cache = {}  # Cache simple pour eviter appels repetes
    
    def geocode_location(self, location_name: str) -> dict:
        """
        Geocodage d'un nom de lieu
        
        Args:
            location_name: Nom du lieu (ex: "Damascus, Syria")
            
        Returns:
            Dictionnaire avec lat, lon, pays
        """
        if location_name in self.cache:
            return self.cache[location_name]
        
        try:
            location = self.geolocator.geocode(location_name, language='en')
            
            if location:
                result = {
                    'latitude': location.latitude,
                    'longitude': location.longitude,
                    'display_name': location.address,
                    'country': location.raw.get('address', {}).get('country', 'unknown')
                }
                self.cache[location_name] = result
                return result
            else:
                return {
                    'latitude': None,
                    'longitude': None,
                    'display_name': None,
                    'country': 'unknown'
                }
                
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            logger.warning(f"Erreur geocodage {location_name}: {e}")
            return {
                'latitude': None,
                'longitude': None,
                'display_name': None,
                'country': 'error'
            }
    
    def enrich_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Enrichissement geospatial d'un DataFrame
        
        Args:
            df: DataFrame avec colonne 'locations' (liste de lieux)
            
        Returns:
            DataFrame avec colonnes lat/lon ajoutees
        """
        logger.info(f"Geocodage de {len(df)} documents")
        
        # Prendre le premier lieu mentionne pour chaque document
        df['primary_location'] = df['locations'].apply(
            lambda x: x[0] if x and len(x) > 0 else None
        )
        
        # Geocodage
        geo_results = df['primary_location'].apply(
            lambda x: self.geocode_location(x) if x else {
                'latitude': None, 'longitude': None, 'country': 'unknown'
            }
        )
        
        df['latitude'] = geo_results.apply(lambda x: x['latitude'])
        df['longitude'] = geo_results.apply(lambda x: x['longitude'])
        df['country'] = geo_results.apply(lambda x: x['country'])
        
        # Stats
        success_rate = df['latitude'].notna().sum() / len(df) * 100
        logger.info(f"Taux de geocodage reussi: {success_rate:.1f}%")
        
        return df


if __name__ == "__main__":
    # Test
    enricher = GeoEnricher()
    print(enricher.geocode_location("Damascus, Syria"))
