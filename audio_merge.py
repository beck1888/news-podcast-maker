import os
import random
import re
from datetime import datetime
from typing import Optional
from pydub import AudioSegment

def sanitize_filename(filename: str) -> str:
    """
    Convert a string into a safe filename by:
    - Removing or replacing invalid characters
    - Converting to lowercase
    - Replacing spaces with underscores
    - Removing multiple consecutive underscores
    """
    # Replace invalid characters with underscore
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Replace spaces and multiple underscores with single underscore
    filename = re.sub(r'[\s_]+', '_', filename)
    # Remove leading/trailing underscores and convert to lowercase
    filename = filename.strip('_').lower()
    # If filename is empty after sanitization, use default
    return filename if filename else 'untitled'

def generate_mixed_audio(speech_path: str, 
                         intro_path: str = "public/news-intro.mp3", 
                         bgm_path: Optional[str] = None, 
                         outro_path: str = "public/news-outro.mp3",
                         title: str = "The Rundown News") -> str:
    """
    Generate the final podcast audio by mixing speech with intro, outro, and background music.
    """
    if bgm_path is None:
        options = [
            'public/background-music_1.mp3',
            'public/background-music_2.mp3',
            'public/background-music_3.mp3'
        ]
        bgm_path = random.choice(options)


    intro = AudioSegment.from_file(intro_path)
    speech = AudioSegment.from_file(speech_path)
    bgm = AudioSegment.from_file(bgm_path)
    outro = AudioSegment.from_file(outro_path)
    
    bgm = bgm - 20
    bgm = bgm.fade_in(1000)

    intro = intro - 10
    outro = outro - 10

    bgm_segments = []
    segment_duration = len(bgm) - 3000
    while sum(len(seg) for seg in bgm_segments) < len(speech):
        segment = bgm[:segment_duration].fade_out(1500).fade_in(1500)
        bgm_segments.append(segment)
    bgm_looped = sum(bgm_segments, AudioSegment.silent(duration=0))[:len(speech)]
    
    fade_out_duration = min(10000, len(bgm_looped))
    bgm_looped = bgm_looped.fade_out(fade_out_duration)
    
    mixed_audio = speech.overlay(bgm_looped)
    final_audio = intro + mixed_audio + outro
    
    clips_dir = os.path.join(os.path.dirname(__file__), 'clips')
    os.makedirs(clips_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    safe_title = sanitize_filename(title)
    output_path = os.path.join(clips_dir, f"{safe_title}_{timestamp}.mp3")
    final_audio.export(output_path, format="mp3")
    
    return output_path

if __name__ == "__main__":
    print("This script is not meant to be run directly. Run main.py instead.")
    exit(1)