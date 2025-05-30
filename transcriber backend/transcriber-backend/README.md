# README.md

# Transcriber Backend

This project is a backend application that downloads Instagram Reel videos, converts them to audio, and transcribes the audio using OpenAI Whisper. It provides a RESTful API for easy integration with other applications.

## Features

- Download Instagram Reels from a provided URL.
- Convert video to audio for transcription.
- Transcribe audio using OpenAI Whisper.
- Return transcription via a Flask HTTP POST endpoint.

## Project Structure

```
transcriber-backend
├── app
│   ├── __init__.py          # Initializes the app package and sets up the Flask application instance.
│   ├── downloader.py        # Contains the function to download Instagram Reel videos.
│   ├── audio_converter.py    # Includes the function to convert video files to audio.
│   ├── transcriber.py       # Defines the Transcriber class for audio transcription.
│   └── utils.py             # Contains utility functions for logging and error handling.
├── celery.py                # Sets up the Celery application for background processing.
├── main.py                  # Entry point of the application, initializes Flask and sets up routes.
├── requirements.txt         # Lists the dependencies required for the project.
├── Dockerfile               # Instructions to build a Docker image for the application.
└── README.md                # Documentation for the project.
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo-name/transcriber-backend.git
   cd transcriber-backend
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the Flask application:
   ```bash
   python main.py
   ```

2. Send a POST request to the `/transcribe` endpoint with a JSON body containing the `reel_url`:
   ```json
   {
       "reel_url": "https://www.instagram.com/reel/your_reel_id/"
   }
   ```

3. The response will include the transcription of the audio extracted from the video.

## API Endpoint

- **POST /transcribe**
  - Request Body:
    - `reel_url`: The URL of the Instagram Reel to be transcribed.
  - Response:
    - `transcription`: The transcribed text from the audio.

## Requirements

- Python 3.7+
- Flask
- instaloader
- moviepy
- openai/whisper
- Redis (for Celery)

## Docker

To build and run the application using Docker, use the following commands:

1. Build the Docker image:
   ```bash
   docker build -t transcriber-backend .
   ```

2. Run the Docker container:
   ```bash
   docker run -p 5000:5000 transcriber-backend
   ```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or features.

## License

This project is licensed under the MIT License. See the LICENSE file for details.