from flask import Flask, request, jsonify
from app.downloader import download_reel
from app.audio_converter import convert_video_to_audio
from app.transcriber import Transcriber
import logging

app = Flask(__name__)
transcriber = Transcriber()

@app.route("/transcribe", methods=["POST"])
def transcribe():
    data = request.get_json()
    reel_url = data.get("reel_url")

    if not reel_url:
        return jsonify({"error": "No reel URL provided"}), 400

    try:
        video_file = download_reel(reel_url)
        audio_file = convert_video_to_audio(video_file)
        transcription = transcriber.transcribe_audio(audio_file)

        return jsonify({
            "transcription": transcription["text"],
            "duration": transcription["duration"],
            "language": transcription["language"]
        })
    except Exception as e:
        logging.error(f"Error during transcription: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)