# Python standard libraries
import os

# Importing the required libraries
from openai import OpenAI

# Importing the local modules
from terminal import Log as log

# Function to translate the script
def translate_text(script: str, target_language: str) -> str:
    # Initialize the OpenAI API
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )
    log.info("OpenAI API Client initialized")

    # Translate the script
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Translate this text into: " + target_language},
            {"role": "user", "content": script}
        ],
        temperature=0.5 # Lower temperature for more accurate translation
    )

    translated_script = response.choices[0].message.content
    log.info("Script translated");

    return translated_script


if __name__ == "__main__":
    # Test the translator
    script = """Hello, this is a test script to be translated. It contains some sample text that needs to be accurately translated into another language."""
    target_language = "Spanish (Mexico)"
    translated_script = translate_text(script, target_language)
    print(translated_script)