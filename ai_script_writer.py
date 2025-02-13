# Python standard libraries
import os
import datetime
import random
from typing import Any, List, Dict, Tuple

# 3rd party imports
from openai import OpenAI

def get_current_date() -> str:
    current_time: datetime.datetime = datetime.datetime.now()
    return current_time.strftime("%A, %B %d, %Y %I:%M %p")

def pick_voice() -> str:
    voices: List[str] = ['alloy', 'ash', 'coral', 'echo', 'fable', 'onyx', 'nova', 'sage', 'shimmer']
    return random.choice(voices)

def get_personality(voicename: str) -> str:
    personalities: Dict[str, str] = {
        'alloy': 'indifferent but informative',
        'ash': 'contemplative and thoughtful',
        'coral': 'dramatic and engaging',
        'echo': 'monotone yet effective',
        'fable': 'quirky and fun',
        'onyx': 'authoritative',
        'nova': 'happy and upbeat',
        'sage': 'hyper and whimsical',
        'shimmer': 'calm and soothing'
    }
    return personalities.get(voicename, "neutral")


def write_script(news: List[Dict[str, str]], language: str = 'en') -> Tuple[str, str]:
    """
    Generates a news script based on the provided top 5 stories.

    Args:
        news (List[Dict[str, str]]): A list of dictionaries, each containing 'publisher', 'headline', and 'content'.
        language (str, optional): The language for the script. Defaults to English ('en').

    Returns:
        Tuple[str, str]: The generated script and the name of the host.
    """
    
    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Get the host's name and personality
    host_name = pick_voice()
    host_personality = get_personality(host_name)
    
    # Define system instructions
    instructions = [
        "You are a news anchor. Write an engaging briefing-style script about the top 5 stories.",
        "Only include text to be spoken aloud without cues or directions.",
        "Include the news outlet for each story.",
        f"It is currently {get_current_date()}. Your name is {host_name} and your personality is {host_personality}. You are a host for The Rundown.",
        "Ensure smooth transitions between stories, and include an introduction and conclusion."
    ]
    
    # Format instructions into system messages
    system_messages = [{"role": "system", "content": instruction} for instruction in instructions]
    
    # Construct the user message with news content
    user_message = {
        "role": "user",
        "content": "\n\n".join(
            [f"{article['publisher']}: {article['headline']}\n{article['content']}" for article in news]
        )
    }
    
    # Send API request
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=system_messages + [user_message],
        temperature=0.7
    )
    
    # Extract the generated script
    script = response.choices[0].message.content

    return script, host_name