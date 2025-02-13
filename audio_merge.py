import os
import tempfile
from pydub import AudioSegment
from datetime import datetime

def generate_mixed_audio(speech_path, intro_path = "public/news-intro.mp3", bgm_path="public/background-music.mp3", outro_path="public/news-outro.mp3"):
    # Load audio files
    intro = AudioSegment.from_file(intro_path)
    speech = AudioSegment.from_file(speech_path)
    bgm = AudioSegment.from_file(bgm_path)
    outro = AudioSegment.from_file(outro_path)
    
    # Adjust background music volume and apply fades
    bgm = bgm - 50  # Reduce volume to be soft
    bgm = bgm.fade_in(1000)  # Quick fade in over 1 second
    
    # Loop background music to match speech length
    bgm_looped = bgm * (len(speech) // len(bgm) + 1)
    bgm_looped = bgm_looped[:len(speech)]  # Trim to exact speech length
    
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
# if __name__ == "__main__":
#     intro = "path/to/intro.mp3"
#     speech = "path/to/speech.mp3"
#     bgm = "path/to/background.mp3"
#     outro = "path/to/outro.mp3"
    
#     output = generate_mixed_audio(intro, speech, bgm, outro)
#     print(f"Generated audio file: {output}")
