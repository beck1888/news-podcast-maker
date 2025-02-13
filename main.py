# Import libraries

# Import built-in libraries
import time

# Import local modules
from terminal import spinner, Log as log
from news_fetcher import fetch_news
from ai_script_writer import write_script
from translate import translate_text
from tts import gen_speech
from audio_merge import generate_mixed_audio

# Settings
log.DO_LOG = False # Global log setting

# Main function
def main() -> None:
    """
    Main function to run the news fetcher.
    """
    start = time.time()
    # log.info("Program ready!")
    # await_press_enter()

    # Clear the terminal
    # clear()

    # Fetch news
    with spinner("Fetching news...", "News fetched!"):
        news = fetch_news()

    # Write script
    with spinner("Writing script...", "Script written!"):
        # We write the script in English because OpenAI's models perform better in English (and the news articles are in English)
        script, voice = write_script(news) #  also catching the voice for the script to use on speech generation

    # Skip this for now so it can run in an automated mode
    # # Translate script to Spanish (for example)
    # if input("Translate script to Spanish? (y/n): ").lower() == "y":
    #     with spinner("Translating script...", "Script translated!"):
    #         script = translate_text(script, "Spanish (Mexico)")
    # else:
    #     log.info("Script not translated")

    # Generate speech
    with spinner("Generating speech...", "Speech generated!"):
        speech_file_path = gen_speech(script, voice)

    # Generate final podcast audio
    with spinner("Generating final audio...", "Final audio generated!"):
        final_audio_path = generate_mixed_audio(speech_file_path)

    print(f"Total time: {time.time() - start:.2f} seconds")
    print(f"Final audio file: {final_audio_path}")

# Entry point
if __name__ == "__main__":
    main()