from flask import jsonify
import whisper
import os
import logging

class Transcriber:
    def __init__(self):
        self.model = whisper.load_model("base")
        logging.basicConfig(level=logging.INFO)
        logging.info("Whisper model loaded successfully.")

    def transcribe_audio(self, audio_file):
        try:
            result = self.model.transcribe(audio_file)
            logging.info("Transcription completed successfully.")
            return {
                "transcription": result["text"],
                "duration": result["duration"],
                "language": result["language"]
            }
        except Exception as e:
            logging.error(f"Error during transcription: {e}")
            return jsonify({"error": "Transcription failed."}), 500