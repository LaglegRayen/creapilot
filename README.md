# CreatorCopilot

A Flask web application that helps YouTube, Instagram, and TikTok creators generate content ideas, analyze transcripts, and generate hashtags.

## Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\\Scripts\\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. (Optional) Create a `.env` file in the project root for environment variables.
4. Run the app:
   ```bash
   python app.py
   ```
5. Open `http://localhost:5000` in your browser.

## Project Structure

- `app.py`: Application factory and blueprint registration.
- `blueprints/`: Feature blueprints for video ideas, transcript analysis, and hashtag assistant.
- `templates/`: Jinja2 templates (`base.html`, `index.html`).
- `static/`:
  - `css/style.css`: Custom styles.
  - `js/main.js`: AJAX logic for feature forms.

## Notes

- Currently uses placeholder AI logic. Replace with free/open-source AI model integration. 