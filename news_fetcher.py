# Built-in/3rd party imports
import os
import requests
from bs4 import BeautifulSoup

# Custom module imports
from terminal import Log as log

def get_full_article(url):
    """
    Fetches and extracts the full text of an article given its URL.
    """
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return "Failed to retrieve full article."
        
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = [p.get_text() for p in soup.find_all("p")]
        return "\n".join(paragraphs)
    except Exception as e:
        log.error(f"Error fetching full article: {e}")
        return "Error retrieving full article."

def fetch_news(country="us", max_articles=5) -> list[dict[str, str]]:
    import time; time.sleep(5) # Tee hee debug me if you can
    """
    Fetches top headlines from NewsAPI for a specified country and returns a structured list of articles. Spinner is recommended for this function.

    :param country: 2-letter ISO 3166-1 code of the country (e.g., 'us' for the United States).
    :param max_articles: Maximum number of articles to fetch.
    :return: List of dictionaries containing publisher, headline, and full content.
    """
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": os.getenv("NEWS_API_KEY"),
        "country": country,
        "pageSize": max_articles + 1,  # Why? Who knows? ¯\_(ツ)_/¯ (it didn't work without this)
    }
    log.info("Endpoint created")

    # Make the call
    response = requests.get(url, params=params)
    if response.status_code != 200:
        log.error("Failed to fetch news: " + str(response.status_code))
        return []
    
    data = response.json()

    if response.status_code != 200 or data.get("status") != "ok":
        log.error("Failed to fetch news: " + data.get("status"))
        return []

    articles = data.get("articles", [])
    if not articles:
        log.warning("No articles fetched. Returning empty list.")
        return []

    structured_articles = []
    
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
    
    log.info("Fetched " + str(len(structured_articles)) + " articles.")
    return structured_articles

def pretty_print(news: list[dict[str, str]]) -> None:
    """
    Pretty prints the news articles.

    :param news: List of dictionaries containing publisher, headline, and full content.
    """
    for i, article in enumerate(news, start=1):
        print(f"{i}. {article['headline']}")
        print(f"   Publisher: {article['publisher']}")
        print(f"   Content: {article['content']}")
        print()

if __name__ == "__main__":
    news = fetch_news()
    pretty_print(news)