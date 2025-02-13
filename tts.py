"""
Text-to-Speech (TTS) module using OpenAI's API.

This module provides functionality to convert text into speech using OpenAI's TTS API.
It handles text splitting, audio generation, and combining multiple audio segments
with appropriate silence intervals between them.

Main features:
- Text to speech conversion using OpenAI's TTS API
- Support for different voices
- Automatic handling of line breaks
- Temporary file management for audio processing
"""

# Python standard libraries
from typing import Any
import uuid
import os
import sys
from pathlib import Path

# 3rd party imports
from openai import OpenAI
from pydub import AudioSegment

def gen_speech(text: str, voice: str = "nova") -> str:
    """
    Generate speech audio from given text using OpenAI TTS API.
    """
    client: Any = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    cache_dir: Path = Path(__file__).parent / ".tmp"
    cache_dir.mkdir(exist_ok=True)

    # Split the text by lines & initialize segments along with silence between segments
    lines = text.split('\n')
    audio_segments: list[AudioSegment] = []
    silence: AudioSegment = AudioSegment.silent(duration=600)

    for line in lines:
        if line.strip():
            response = client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=line
            )
            temp_file_path: Path = cache_dir / f"{uuid.uuid4()}.mp3"
            response.write_to_file(temp_file_path)
            audio_segments.append(AudioSegment.from_mp3(temp_file_path))

    combined_audio: AudioSegment = AudioSegment.empty()
    for segment in audio_segments:
        combined_audio += segment + silence

    final_file_path: Path = cache_dir / f"{uuid.uuid4()}.mp3"
    combined_audio.export(final_file_path, format="mp3")
    return str(final_file_path)

if __name__ == "__main__":
    print("This script is not meant to be run directly. Run main.py instead.")
    sys.exit(1)
