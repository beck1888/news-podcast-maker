# Python standard libraries
import os
import datetime
import random

# Importing the required libraries
from openai import OpenAI

# Importing the local modules
from terminal import Log as log

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
    return personalities

# Function to write the script
def write_script(news: list[dict[str, str]], language: str = 'en') -> list[dict[str, str]]:
    # Initialize the OpenAI API
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )
    log.info("OpenAI API Client initialized")

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
    log.info("Script written")

    # Log the script in case it has warnings (possible openai content violations - idk yet but anything with like violence could be bad) and needs to be reviewed by a human
    log_filename = datetime.datetime.now().strftime("logs/script_%Y_%m_%d_%H_%M_%S.log") # Log file name with timestamp as filesafe chars
    with open(log_filename, 'w') as f:
        f.write(get_current_date()) # Add the current date and time for reference
        f.write('\n\n') # Add a newline for readability
        f.write(str(full_api_response)) # Because otherwise it'll just be the text not the metadata which is useless!
        f.write('\n\n') # Add a newline for readability


    return script, hosts_name # Return the script and the host's name both for use in the audio generation


if __name__ == "__main__":
    # Test the summarizer
    news = [
        {
            "publisher": "BBC",
            "headline": "Goats are taking over the world",
            "content": "In a shocking turn of events, goats have started to take over the world. They have been seen in various cities, eating everything in sight. Scientists are baffled by this sudden change in behavior."
        },
        {
            "publisher": "CNN",
            "headline": "Here's why you should never trust a cat",
            "content": "Cats have long been known for their cunning and deceitful ways. A new study has found that cats are actually plotting to take over the world. They have been secretly communicating with each other and planning their next move."
        }
    ]

    script = write_script(news)
    print(script)