# Python standard libraries
import os
import datetime
import random

# Importing the required libraries
from openai import OpenAI

# Helper functions
def get_current_date() -> str:
    """
    Gets the current date and time in a human-readable format.
    """
    return datetime.datetime.now().strftime("%A, %B %d, %Y %I:%M %p")

def pick_voice() -> str:
    voices = ['alloy', 'ash', 'coral', 'echo', 'fable', 'onyx', 'nova', 'sage', 'shimmer']
    return random.choice(voices)

def get_personality(voicename: str) -> str:
    personalities = {
        'alloy': 'indifferent but informative ',
        'ash': 'contemplative and thoughtful',
        'coral': 'dramatic and engaging',
        'echo': 'monotone yet effective',
        'fable': 'quirky and fun',
        'onyx': 'authoritative',
        'nova': 'happy and upbeat',
        'sage': 'hyper and whimsical',
        'shimmer': 'calm and soothing'
    }
    return personalities[voicename]

# Function to write the script
def write_script(news: list[dict[str, str]], language: str = 'en') -> tuple[list[dict[str, str]], str]:
    # Initialize the OpenAI API
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )

    # Get the host's name
    hosts_name = pick_voice()

    # Write the script
    full_api_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a news anchor. Write an engaging and well flowing briefing style script informing the audience about the following top 5 stories they need to know."},
            {"role": "system", "content": "Only write the parts to be spoken aloud. Do not include cues, directions, who's speaking, etc."},
            {"role": "system", "content": "Include which news outlet each story is from."},
            {"role": "system", "content": f"Use the following info to tailor the script to the audience: It is currently {get_current_date()}. Your name is {hosts_name}. Your personality is {get_personality(hosts_name)} You are a host for the news channel: The Rundown."},
            {"role": "system", "content": "Make sure to include a smooth transition between each story. Include an introduction and conclusion as well."},
            {"role": "user", "content": "\n\n".join([f"{article['publisher']}: {article['headline']}\n{article['content']}" for article in news])}
        ],
        temperature=0.7 # Higher temperature means more randomness but better creativity (might be bad for news - we'll see)
    )
    script = full_api_response.choices[0].message.content

    return script, hosts_name # Return the script and the host's name both for use in the audio generation