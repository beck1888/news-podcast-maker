"""
Audio processing module for news podcast generation.
Handles mixing of speech audio with intro/outro segments and background music,
including file name sanitization and proper audio level adjustments.
"""

import os
import random
import re
import sys
from datetime import datetime
from typing import Optional, List
from pydub import AudioSegment

def sanitize_filename(filename: str) -> str:
    """
    Convert a string into a readable filename by:
    - Properly capitalizing words
    - Formatting date in parentheses
    - Removing timestamp from the end
    - Adding .mp3 extension
    """
    # Remove any existing timestamp pattern at the end
    filename = re.sub(r'_\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}$', '', filename)

    # Replace underscores with spaces
    filename = filename.replace('_', ' ')

    # Capitalize words properly
    words: List[str] = filename.split()
    capitalized_words: List[str] = []
    for word in words:
        # Don't capitalize certain small words unless they're at the start
        if (word.lower() not in ['the', 'and', 'in', 'on', 'at', 'to', 'for', 'of']
            or not capitalized_words):
            word = word.capitalize()
        else:
            word = word.lower()
        capitalized_words.append(word)

    # Join words back together
    filename = ' '.join(capitalized_words)

    # Extract date if present in the original filename
    date_match: Optional[re.Match] = re.search(r'\d{4}-\d{2}-\d{2}', filename)
    if date_match:
        date_str: str = date_match.group()
        date_obj: datetime = datetime.strptime(date_str, '%Y-%m-%d')
        formatted_date: str = date_obj.strftime('%b %d %Y')
        # Remove the original date from the filename
        filename = re.sub(r'\d{4}-\d{2}-\d{2}', '', filename)
        # Add formatted date in parentheses
        filename = f"{filename.strip()} - ({formatted_date})"

    # Clean up any remaining special characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)

    # Remove multiple spaces and trim
    filename = re.sub(r'\s+', ' ', filename).strip()

    # Add .mp3 extension
    filename = f"{filename}.mp3"

    return filename if filename else 'untitled.mp3'

def generate_mixed_audio(speech_path: str,
                         intro_path: str = "public/news-intro.mp3",
                         bgm_path: Optional[str] = None,
                         outro_path: str = "public/news-outro.mp3",
                         title: str = "The Rundown News") -> str:
    """
    Generate the final podcast audio by mixing speech with intro, outro, and background music.
    """
    if bgm_path is None:
        bgm_path = random.choice([
            'public/background-music_1.mp3',
            'public/background-music_2.mp3',
            'public/background-music_3.mp3'
        ])

    # Load audio segments
    audio_segments = {
        'intro': AudioSegment.from_file(intro_path),
        'speech': AudioSegment.from_file(speech_path),
        'bgm': AudioSegment.from_file(bgm_path),
        'outro': AudioSegment.from_file(outro_path)
    }

    # Adjust volume levels
    audio_segments['bgm'] = audio_segments['bgm'].fade_in(1000) - 20
    audio_segments['intro'] -= 10
    audio_segments['outro'] -= 10

    # Create looped background music
    bgm_loop = AudioSegment.silent(duration=0)
    segment_duration = len(audio_segments['bgm']) - 3000

    while len(bgm_loop) < len(audio_segments['speech']):
        segment = audio_segments['bgm'][:segment_duration].fade_out(1500).fade_in(1500)
        bgm_loop += segment

    bgm_loop = bgm_loop[:len(audio_segments['speech'])]
    fade_out_duration = min(10000, len(bgm_loop))
    bgm_loop = bgm_loop.fade_out(fade_out_duration)

    # Mix audio
    mixed_audio = audio_segments['speech'].overlay(bgm_loop)
    final_audio = audio_segments['intro'] + mixed_audio + audio_segments['outro']

    # Export final audio
    clips_dir = os.path.join(os.path.dirname(__file__), 'clips')
    os.makedirs(clips_dir, exist_ok=True)
    output_path = os.path.join(
        clips_dir,
        f"{sanitize_filename(title)}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.mp3"
    )
    final_audio.export(output_path, format="mp3")

    return output_path

if __name__ == "__main__":
    print("This script is not meant to be run directly. Run main.py instead.")
    sys.exit(1)
