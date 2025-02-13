# Import libraries

# Import built-in libraries

# Import local modules
from terminal import spinner, Log as log
from news_fetcher import fetch_news
from ai_script_writer import write_script
from translate import translate_text

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

    # Write script
    with spinner("Writing script...", "Script written!"):
        script = write_script(news) # We write the script in English because OpenAI's models perform better in English (and the news articles are in English)

    # This is something we can implement in the future - but this code does work as is just needs polish and proper implementation
    # # Translate script to Spanish (for example)
    # with spinner("Translating script...", "Script translated!"):
    #     translated_script = translate_text(script, "Spanish (Mexico)")

    # Print the script
    print(script)

# Entry point
if __name__ == "__main__":
    main()