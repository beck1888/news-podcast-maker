# Import libraries

# Import built-in libraries

# Import local modules
from terminal import spinner, Log as log
from news_fetcher import fetch_news

# Settings
log.DO_LOG = False # Global log setting

# Main function
def main() -> None:
    """
    Main function to run the news fetcher.
    """
    # log.info("Program ready!")
    # await_press_enter()

    # Clear the terminal
    # clear()

    # Fetch news
    with spinner("Fetching news...", "News fetched!"):
        news = fetch_news()

    # Print news
    print(news)

# Entry point
if __name__ == "__main__":
    main()