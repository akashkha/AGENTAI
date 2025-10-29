import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import time
import json
import os

class SearchEngine:
    def __init__(self):
        self.cache_file = os.path.join(os.path.dirname(__file__), 'search_cache.json')
        self.cache = self._load_cache()
        self.search_delay = 1  # Delay between searches to respect rate limits

    def _load_cache(self) -> Dict:
        """Load search cache from file"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def _save_cache(self):
        """Save search cache to file"""
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f)

    def search(self, query: str, category: Optional[str] = None) -> List[Dict]:
        """
        Search for information using multiple sources
        Returns a list of relevant results
        """
        cache_key = f"{category}_{query}" if category else query
        
        # Check cache first
        if cache_key in self.cache:
            return self.cache[cache_key]

        sources = []
        if category == "coding":
            sources = [
                "stackoverflow.com",
                "github.com",
                "leetcode.com",
                "hackerrank.com",
                "geeksforgeeks.org"
            ]
        elif category == "interview":
            sources = [
                "glassdoor.com",
                "indeed.com",
                "linkedin.com",
                "interviewbit.com",
                "careercup.com"
            ]
        else:
            sources = [
                "stackoverflow.com",
                "github.com",
                "medium.com",
                "dev.to",
                "glassdoor.com"
            ]

        results = []
        for source in sources:
            search_url = f"https://www.google.com/search?q=site:{source} {query}"
            
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                response = requests.get(search_url, headers=headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract search results
                search_results = soup.find_all('div', class_='g')
                
                for result in search_results[:3]:  # Get top 3 results from each source
                    title_elem = result.find('h3')
                    link_elem = result.find('a')
                    snippet_elem = result.find('div', class_='VwiC3b')
                    
                    if title_elem and link_elem and snippet_elem:
                        results.append({
                            'title': title_elem.text,
                            'link': link_elem['href'],
                            'snippet': snippet_elem.text,
                            'source': source
                        })
                
                time.sleep(self.search_delay)  # Respect rate limits
                
            except Exception as e:
                print(f"Error searching {source}: {str(e)}")
                continue

        # Cache the results
        self.cache[cache_key] = results
        self._save_cache()
        
        return results

    def get_coding_solutions(self, question: str) -> List[Dict]:
        """
        Search for alternative solutions to coding questions
        """
        return self.search(f"solution to {question} programming", category="coding")

    def format_results(self, results: List[Dict]) -> str:
        """
        Format search results into readable text
        """
        if not results:
            return "No results found."
        
        formatted = "Search Results:\n\n"
        
        for idx, result in enumerate(results, 1):
            formatted += f"{idx}. {result['title']}\n"
            formatted += f"   Source: {result['source']}\n"
            formatted += f"   {result['snippet']}\n\n"
            
        return formatted