import os

import requests
from dotenv import load_dotenv


class ResearchAgent:
    def __init__(self, topic):
        self.topic = topic
        load_dotenv()

    def run(self, max_results=5):
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key :
            raise RuntimeError("Set TAVILY_API_KEY in your .env file before running the app.")

        search_payloads = [
            {
                "query": self.topic, 
                "search_depth": "basic",
                "max_results": max_results,
                "include_answer": False,
                "include_raw_content": False,
            },
            {
                "query": (
                    f"{self.topic} existing research work methods systems datasets "
                    "limitations future scope"
                ),
                "search_depth": "basic",
                "max_results": max_results,
                "include_answer": False,
                "include_raw_content": False,
            },
            {
                "query": f"{self.topic} research papers studies",
                "search_depth": "basic",
                "max_results": max_results,
                "include_answer": False,
                "include_raw_content": False,
                "include_domains": [
                    "arxiv.org",
                    "pubmed.ncbi.nlm.nih.gov",
                    "semanticscholar.org",
                    "researchgate.net",
                ],
            },
        ]

        for payload in search_payloads:
            papers = self._search_tavily(api_key, payload)
            if papers:
                return papers

        raise RuntimeError("No Tavily results found. Try a broader research topic.")

    def _search_tavily(self, api_key, payload):
        response = requests.post(
            "https://api.tavily.com/search",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30,
        )
        response.raise_for_status()

        papers = []
        for item in response.json().get("results", []):
            content = item.get("raw_content") or item.get("content") or "No summary available."
            papers.append({
                "title": item.get("title", "Untitled result"),
                "abstract": content,
                "url": item.get("url", ""),
                "authors": [],
                "published": "Unknown",
            })

        return papers
