import os
import random
import re
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
        if word.lower() not in ['the', 'and', 'in', 'on', 'at', 'to', 'for', 'of'] or not capitalized_words:
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
        options: List[str] = [
            'public/background-music_1.mp3',
            'public/background-music_2.mp3',
            'public/background-music_3.mp3'
        ]
        bgm_path = random.choice(options)

    intro: AudioSegment = AudioSegment.from_file(intro_path)
    speech: AudioSegment = AudioSegment.from_file(speech_path)
    bgm: AudioSegment = AudioSegment.from_file(bgm_path)
    outro: AudioSegment = AudioSegment.from_file(outro_path)
    
    bgm = bgm - 20
    bgm = bgm.fade_in(1000)

    intro = intro - 10
    outro = outro - 10

    bgm_segments: List[AudioSegment] = []
    segment_duration: int = len(bgm) - 3000
    while sum(len(seg) for seg in bgm_segments) < len(speech):
        segment: AudioSegment = bgm[:segment_duration].fade_out(1500).fade_in(1500)
        bgm_segments.append(segment)
    bgm_looped: AudioSegment = sum(bgm_segments, AudioSegment.silent(duration=0))[:len(speech)]
    
    fade_out_duration: int = min(10000, len(bgm_looped))
    bgm_looped = bgm_looped.fade_out(fade_out_duration)
    
    mixed_audio: AudioSegment = speech.overlay(bgm_looped)
    final_audio: AudioSegment = intro + mixed_audio + outro
    
    clips_dir: str = os.path.join(os.path.dirname(__file__), 'clips')
    os.makedirs(clips_dir, exist_ok=True)
    timestamp: str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    safe_title: str = sanitize_filename(title)
    output_path: str = os.path.join(clips_dir, f"{safe_title}_{timestamp}.mp3")
    final_audio.export(output_path, format="mp3")
    
    return output_path

if __name__ == "__main__":
    print("This script is not meant to be run directly. Run main.py instead.")
    exit(1)