"""Web search integration"""
import requests
from typing import List, Dict, Optional
import logging
from config import GOOGLE_API_KEY, GOOGLE_SEARCH_ENGINE_ID

logger = logging.getLogger(__name__)


def search_web(query: str, num_results: int = 5) -> List[Dict]:
    """Search the web using Google Custom Search API"""
    
    if not GOOGLE_API_KEY or not GOOGLE_SEARCH_ENGINE_ID:
        logger.warning("Google API keys not configured")
        return search_web_fallback(query, num_results)
    
    try:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "q": query,
            "key": GOOGLE_API_KEY,
            "cx": GOOGLE_SEARCH_ENGINE_ID,
            "num": num_results
        }
        
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        results = []
        
        if "items" in data:
            for item in data["items"]:
                results.append({
                    "title": item.get("title", ""),
                    "link": item.get("link", ""),
                    "snippet": item.get("snippet", "")
                })
        
        return results
        
    except Exception as e:
        logger.error(f"Google search error: {e}")
        return search_web_fallback(query, num_results)


def search_web_fallback(query: str, num_results: int = 3) -> List[Dict]:
    """Fallback web search using DuckDuckGo"""
    try:
        url = "https://api.duckduckgo.com/"
        params = {
            "q": query,
            "format": "json"
        }
        
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        results = []
        
        # Get results from related topics
        if "RelatedTopics" in data:
            for item in data["RelatedTopics"][:num_results]:
                if "FirstURL" in item:
                    results.append({
                        "title": item.get("Text", ""),
                        "link": item.get("FirstURL", ""),
                        "snippet": item.get("Text", "")
                    })
        
        return results
        
    except Exception as e:
        logger.error(f"Fallback search error: {e}")
        return []


def search_image(query: str) -> List[str]:
    """Search for images"""
    # Implementation would depend on image search API
    return []
