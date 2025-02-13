# Import libraries

# Import built-in libraries

# Import local modules
from terminal import spinner, Log as log
from news_fetcher import fetch_news
from ai_script_writer import write_script
from translate import translate_text
from tts import gen_speech

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

    # Translate script to Spanish (for example)
    if input("Translate script to Spanish? (y/n): ").lower() == "y":
        with spinner("Translating script...", "Script translated!"):
            script = translate_text(script, "Spanish (Mexico)")
    else:
        log.info("Script not translated")

    # Generate speech
    with spinner("Generating speech...", "Speech generated!"):
        speech_file_path = gen_speech(script)

    # Print the speech file path
    print(speech_file_path)

# Entry point
if __name__ == "__main__":
    main()