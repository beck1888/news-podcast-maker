from openai import OpenAI
from pathlib import Path
import uuid
import os
from pydub import AudioSegment

def gen_speech(text, voice="nova") -> str:
    # Initialize the OpenAI API client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Create the cache directory if it doesn't exist
    if not os.path.exists(Path(__file__).parent / "cache"):
        os.makedirs(Path(__file__).parent / "cache")

    # Split the text by line breaks
    lines = text.split('\n')
    audio_segments = []
    silence = AudioSegment.silent(duration=600)  # 0.6 seconds of silence

    for line in lines:
        if line.strip():  # Skip empty lines
            # Structure the request
            response = client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=line
            )

            # Save the audio file
            temp_file_path = Path(__file__).parent / "cache" / f"{uuid.uuid4()}.mp3"
            response.write_to_file(temp_file_path)
            audio_segments.append(AudioSegment.from_mp3(temp_file_path))

    # Combine all audio segments into one with 0.6 seconds of silence between each
    combined_audio = AudioSegment.empty()
    for segment in audio_segments:
        combined_audio += segment + silence

    # Save the combined audio file
    final_file_path = Path(__file__).parent / "cache" / f"{uuid.uuid4()}.mp3"
    combined_audio.export(final_file_path, format="mp3")

    return final_file_path

if __name__ == "__main__":
    print(gen_speech("Hello, world!\nThis is a test."))  # Should return a path to a file with the combined speech