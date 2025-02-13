import os
from openai import OpenAI

def translate_text(script: str, target_language: str) -> str:
    """
    Translate the given script into target_language.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"Translate this text into: {target_language}"},
            {"role": "user", "content": script}
        ],
        temperature=0.5 # Slightly lower temperature to ensure more accurate translations
    )

    translated_script: str = response.choices[0].message.content
    return translated_script