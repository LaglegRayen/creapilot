from moviepy.editor import VideoFileClip
import os

def convert_video_to_audio(video_file):
    try:
        audio_file = "audio.wav"
        clip = VideoFileClip(video_file)
        clip.audio.write_audiofile(audio_file)
        return audio_file
    except Exception as e:
        raise RuntimeError(f"Error converting video to audio: {e}") from e
    finally:
        if os.path.exists(video_file):
            os.remove(video_file)