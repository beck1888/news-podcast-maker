# Python standard libraries
import os
import datetime

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

# Function to write the script
def write_script(news: list[dict[str, str]]) -> list[dict[str, str]]:
    # Initialize the OpenAI API
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )
    log.info("OpenAI API Client initialized")

    # Write the script
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a news anchor. Write a daily briefing style script informing the audience about the following top 5 stories they need to know."},
            {"role": "system", "content": "Only write the parts to be spoken aloud. Do not include cues, directions, who's speaking, etc."},
            {"role": "system", "content": "Include who the article is from for each story."},
            {"role": "system", "content": f"Use the following info to tailor the script to the audience: It is currently {get_current_date()}. Your name is Axel. You are the host for Atom News."},
            {"role": "user", "content": "\n\n".join([article["content"] for article in news])}
        ],
        temperature=0.4
    )
    script = response.choices[0].message.content
    log.info("Script written")

    return script

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