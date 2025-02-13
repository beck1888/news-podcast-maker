import os
import tempfile
from pydub import AudioSegment
from datetime import datetime
import random

def generate_mixed_audio(speech_path, intro_path = "public/news-intro.mp3", bgm_path=None, outro_path="public/news-outro.mp3"):
    # Get random background music if not provided
    if bgm_path is None:
        options = [
            'public/background-music_1.mp3',
            'public/background-music_2.mp3',
            'public/background-music_3.mp3'
        ]
        bgm_path = random.choice(options)
    
    
    # Load audio files
    intro = AudioSegment.from_file(intro_path)
    speech = AudioSegment.from_file(speech_path)
    bgm = AudioSegment.from_file(bgm_path)
    outro = AudioSegment.from_file(outro_path)
    
    # Adjust background music volume and apply fades
    bgm = bgm - 20  # Reduce volume to be soft
    bgm = bgm.fade_in(1000)  # Quick fade in over 1 second

    # Reduce volume of intro and outro
    intro = intro - 10
    outro = outro - 10
    
    # Loop background music to match speech length with seamless fades
    bgm_segments = []
    segment_duration = len(bgm) - 3000  # Duration minus 3 seconds for fade out/in
    while sum(len(segment) for segment in bgm_segments) < len(speech):
        segment = bgm[:segment_duration].fade_out(1500).fade_in(1500)
        bgm_segments.append(segment)
    bgm_looped = sum(bgm_segments, AudioSegment.silent(duration=0))[:len(speech)]  # Trim to exact speech length
    
    # Apply fade out 10 seconds before the end
    fade_out_duration = min(10000, len(bgm_looped))  # Ensure fade duration is not longer than the track
    bgm_looped = bgm_looped.fade_out(fade_out_duration)
    
    # Overlay background music onto speech
    mixed_audio = speech.overlay(bgm_looped)
    
    # Concatenate all parts together
    final_audio = intro + mixed_audio + outro
    
    # Save to clips directory
    clips_dir = os.path.join(os.path.dirname(__file__), 'clips')
    os.makedirs(clips_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_path = os.path.join(clips_dir, f"News_Podcast_{timestamp}.mp3")
    final_audio.export(output_path, format="mp3")
    
    return output_path

# # Example usage
if __name__ == "__main__":
    output = generate_mixed_audio('/Users/beckorion/Documents/Python/news-podcast-maker/cache/adf4199e-68a5-45b5-a8bf-f1bd7aa159fd.mp3')
    print(f"Generated audio file: {output}")
