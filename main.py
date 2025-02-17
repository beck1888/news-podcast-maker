"""
News Podcast Maker - A tool to automatically generate news podcasts.
This module serves as the main entry point, orchestrating the process
of fetching news, generating scripts, and creating audio content.
"""
# Python standard libraries
import time
import os
from typing import List, Dict, Any

# Import local modules
from terminal import spinner
from news_fetcher import fetch_news
from ai_script_writer import write_script
from tts import gen_speech
from audio_merge import generate_mixed_audio
from cleanup import cleanup_directory

# Main function
def main() -> None:
    """
    Main function to run the news podcast maker.
    """
    start: float = time.time()

    # Fetch news
    with spinner("Fetching news...", "News fetched!"):
        news: List[Dict[str, Any]] = fetch_news()

    # Write script
    with spinner("Writing script...", "Script written!"):
        script: str
        voice: str
        script, voice, headline = write_script(news)

    # # Translate script to another language (optional)
    # with spinner("Translating script...", "Script translated!"):
    #     target_language: str = "Spanish"  # Example - use full language name
    #     script: str = translate_text(script, target_language)

    # Generate speech
    with spinner("Synthesizing speech...", "Speech synthesized!"):
        speech_file_path: str = gen_speech(script, voice)

    # Generate final podcast audio
    with spinner("Generating final audio...", "Final audio generated!"):
        # The clip is also saved in the 'clips' directory as backup
        final_audio_path: str = generate_mixed_audio(speech_file_path, title=headline.capitalize())

    # Cleanup temporary files
    with spinner("Cleaning up temporary files...", "Temporary files cleaned!"):
        cleanup_directory() # Cleanup all temporary files by default

    # Clone the final audio file to the user's downloads folder (assuming macOS)
    # os.system(f"cp {final_audio_path} ~/Downloads")

    # Print final details
    print(f"Total time: {time.time() - start:.2f} seconds")
    print(f"Final audio file: '{final_audio_path}'")
    # print("The final audio file has been copied to your Downloads folder.")

    # Open the final audio file
    # os.system(f"open {final_audio_path}")

# Entry point
if __name__ == "__main__":
    main()
