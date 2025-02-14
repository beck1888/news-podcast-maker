"""
Module for fetching and processing news articles from NewsAPI.
Provides functionality to retrieve full articles and format them for further processing.
"""

# Python Standard Libraries
import os
import sys
from typing import List, Dict

# 3rd party imports
import requests
from bs4 import BeautifulSoup


def get_full_article(url: str) -> str:
    """
    Fetch and extract the full text of an article given its URL.
    """
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return "Failed to retrieve full article."

        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = [p.get_text() for p in soup.find_all("p")]
        return "\n".join(paragraphs)
    except requests.RequestException as e:
        return "Failed to retrieve full article. Just read the headline and existing content instead and move on."

def fetch_news(country: str = "us", max_articles: int = 5) -> List[Dict[str, str]]:
    """
    Fetches top headlines from NewsAPI for a country and returns a structured list of articles.
    Spinner is recommended for this function.

    :param country: 2-letter ISO 3166-1 code of the country (e.g., 'us' for the United States)
    :param max_articles: Maximum number of articles to fetch
    :return: List of dictionaries containing publisher, headline, and full content
    """
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": os.getenv("NEWS_API_KEY"),
        "country": country,
        "pageSize": max_articles + 1,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if response.status_code != 200 or data.get("status") != "ok":
            raise requests.RequestException(
                f"Failed to fetch news: {data.get('message', 'Unknown error')}"
            )

        articles = data.get("articles", [])
        if not articles:
            raise ValueError("No articles found in response")

        structured_articles: List[Dict[str, str]] = []

        for article in articles:
            publisher = article.get("source", {}).get("name", "Unknown Publisher")
            headline = article.get("title", "No title available")
            url = article.get("url", "")

            full_content = get_full_article(url) if url else "No URL available."

            structured_articles.append({
                "publisher": publisher,
                "headline": headline,
                "content": full_content
            })

        return structured_articles
    except requests.RequestException as e:
        raise requests.RequestException(f"API request failed: {str(e)}") from e

def pretty_print(news: List[Dict[str, str]]) -> None:
    """
    Pretty prints the news articles.

    :param news: List of dictionaries containing publisher, headline, and full content
    """
    for i, article in enumerate(news, start=1):
        print(f"{i}. {article['headline']}")
        print(f"   Publisher: {article['publisher']}")
        print(f"   Content: {article['content']}")
        print()

if __name__ == "__main__":
    print("This script is not meant to be run directly. Run main.py instead.")
    sys.exit(1)
