\"\"\"
Module d'extraction Twitter/X via snscrape
\"\"\"

import pandas as pd
import snscrape.modules.twitter as sntwitter
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TwitterCollector:
    \"\"\"
    Collecteur de données Twitter pour surveillance OSINT
    \"\"\"
    
    def __init__(self, max_results: int = 1000):
        self.max_results = max_results
        logger.info(f\"Initialisation TwitterCollector (max: {max_results})\")
    
    def search_by_keywords(
        self, 
        keywords: List[str], 
        start_date: str, 
        end_date: str,
        language: str = 'en'
    ) -> pd.DataFrame:
        \"\"\"
        Recherche de tweets par mots-clés dans une période
        
        Args:
            keywords: Liste des termes de recherche
            start_date: Date début (YYYY-MM-DD)
            end_date: Date fin (YYYY-MM-DD)
            language: Code langue ISO
            
        Returns:
            DataFrame avec les tweets collectés
        \"\"\"
        query = f\"({' OR '.join(keywords)}) since:{start_date} until:{end_date} lang:{language}\"
        logger.info(f\"Requete: {query}\")
        
        tweets = []
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
            if i >= self.max_results:
                break
            
            tweets.append({
                'id': tweet.id,
                'date': tweet.date,
                'content': tweet.rawContent,
                'username': tweet.user.username,
                'url': tweet.url,
                'reply_count': tweet.replyCount,
                'retweet_count': tweet.retweetCount,
                'like_count': tweet.likeCount,
                'language': tweet.lang,
                'source': 'twitter'
            })
        
        df = pd.DataFrame(tweets)
        logger.info(f\"Collectes: {len(df)} tweets")
        return df
    
    def search_by_geolocation(
        self,
        lat: float,
        lon: float,
        radius_km: int,
        keywords: List[str] = None
    ) -> pd.DataFrame:
        \"\"\"
        Recherche geolocalisee (zone de crise)
        
        Args:
            lat: Latitude centre
            lon: Longitude centre
            radius_km: Rayon en kilometres
            keywords: Filtres additionnels
            
        Returns:
            DataFrame tweets geolocalises
        \"\"\"
        geo_filter = f\"geocode:{lat},{lon},{radius_km}km\"
        query = f\"({' OR '.join(keywords)}) {geo_filter}\" if keywords else geo_filter
        
        logger.info(f\"Recherche geo: {query}\")
        
        tweets = []
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
            if i >= self.max_results:
                break
            
            tweets.append({
                'id': tweet.id,
                'date': tweet.date,
                'content': tweet.rawContent,
                'username': tweet.user.username,
                'url': tweet.url,
                'latitude': tweet.coordinates.latitude if tweet.coordinates else None,
                'longitude': tweet.coordinates.longitude if tweet.coordinates else None,
                'source': 'twitter_geo'
            })
        
        return pd.DataFrame(tweets)


if __name__ == \"__main__\":
    # Test
    collector = TwitterCollector(max_results=10)
    df = collector.search_by_keywords(
        keywords=['Ukraine'],
        start_date='2024-01-01',
        end_date='2024-01-02'
    )
    print(df.head())
