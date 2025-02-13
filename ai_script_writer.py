"""Module for AI script writing for the news podcast maker."""
# Python standard libraries
import sys  # Added for sys.exit
import os
import datetime
import random
from typing import List, Dict, Tuple  # Removed unused Any

# 3rd party imports
from openai import OpenAI

def get_current_date() -> str:
    """Return the current date and time as a formatted string."""
    current_time: datetime.datetime = datetime.datetime.now()
    return current_time.strftime("%A, %B %d, %Y %I:%M %p")

def pick_voice() -> str:
    """Pick a random voice from a predefined list excluding 'coral'."""
    voices: List[str] = [
        'alloy', 'ash', 'coral', 'echo', 'fable',
        'onyx', 'nova', 'sage', 'shimmer'
    ]
    voices.remove('coral')  # Remove Coral because it is too dramatic
    return random.choice(voices)

def get_personality(voicename: str) -> str:
    """Return the personality description for the given voice name."""
    default_personality: str = 'neutral and balanced, adapting to context'
    personalities: Dict[str, str] = {
        'alloy': ("neutral and pragmatic, delivering information with a straightforward "
                  "and no-nonsense tone"),
        'ash': ("philosophical and introspective, often pondering deeper meanings and "
                "abstract ideas"),
        'coral': ("expressive and theatrical, speaking with passion and a flair for "
                  "storytelling"),
        'echo': ("robotic and efficient, conveying information in a precise and "
                 "calculated manner"),
        'fable': "witty and playful, often using humor and charm to engage in conversations",
        'onyx': "commanding and authoritative, exuding confidence and certainty in speech",
        'nova': ("cheerful and energetic, always enthusiastic and ready to uplift any "
                 "conversation"),
        'sage': ("eccentric and whimsical, with a lively imagination and a penchant for the "
                 "unexpected"),
        'shimmer': "gentle and serene, speaking in a soothing and reassuring manner"
    }
    return personalities.get(voicename, default_personality) # Return the personality or default

def create_headline_for_podcast(script: str) -> str:
    """
    Create a creative title for this podcast episode based on the provided script.
    """
    # Initialize the client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    instructions: list = [
        "Create a creative title for this podcast episode based on the script provided.",
        "The title should be between 5-10 words long and should be engaging and informative.",
        "Only include the title. Do not include any other information."
    ]

    # Format instructions into the messages
    system_messages = [{"role": "system", "content": instruction} for instruction in instructions]

    # Construct the user message with the script content
    user_message = {
        "role": "user",
        "content": script
    }

    # Send the API request
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=system_messages + [user_message],
        temperature=0.7
    )

    # Extract the generated title
    title = response.choices[0].message.content

    # Append the date to the title
    title += f" - {get_current_date()}"

    return title

def write_script(news: List[Dict[str, str]], language: str = 'en') -> Tuple[str, str, str]:
    """
    Generates a news script based on the provided top 5 stories.

    Args:
        news (List[Dict[str, str]]): A list of dictionaries, each containing 'publisher', 
        'headline', and 'content'.
        language (str, optional): The language for the script. Defaults to English ('en').

    Returns:
        Tuple[str, str]: The generated script, the host's name, and the headline.
    """
    _ = language  # Mark language as used to avoid unused argument warning

    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Get the host's name and personality
    host_name = pick_voice()
    host_personality = get_personality(host_name)

    # Define system instructions
    instructions: list = [
        "You are a news anchor. Write an engaging briefing-style script about the top 5 stories.",
        "Only include text to be spoken aloud without cues or directions.",
        "Include the news outlet for each story.",
        (f"It is currently {get_current_date()}. Your name is {host_name} and your personality is "
         f"{host_personality}. You are a host for The Rundown."),
        "Ensure smooth transitions between stories, and include an introduction and conclusion.",
        "Add 2 new lines between each story and section for clarity."
    ]

    # Format instructions into system messages
    system_messages = [{"role": "system", "content": instruction} for instruction in instructions]

    # Construct the user message with news content split over multiple lines to reduce width
    user_message = {
        "role": "user",
        "content": "\n\n".join([
            f"{article['publisher']}: {article['headline']}\n{article['content']}"
            for article in news
        ])
    }

    # Send API request
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=system_messages + [user_message],
        temperature=0.7
    )

    # Extract the generated script
    script = response.choices[0].message.content

    # Generate a headline for the podcast episode
    headline = create_headline_for_podcast(script)

    return script, host_name, headline

if __name__ == "__main__":
    print("This script is not meant to be run directly. Run main.py instead.")
    sys.exit(1)
