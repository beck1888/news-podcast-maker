from openai import OpenAI
from pathlib import Path
import uuid
import os

def gen_speech(text, voice="nova") -> str: # We should probably use a .cache directory for this instead of the root directory cache regular file but oh well
    # Initialize the OpenAI API client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Structure the request
    response = client.audio.speech.create(
    model="tts-1", # Not 'HD' because that's expensive
    voice=voice,
    input=text
    )

    # Create the cache directory if it doesn't exist
    if not os.path.exists(Path(__file__).parent / "cache"):
        os.makedirs(Path(__file__).parent / "cache")

    # Save the audio file
    file_name = speech_file_path = Path(__file__).parent / "cache" / f"{uuid.uuid4()}.mp3"
    response.write_to_file(speech_file_path)

    return speech_file_path