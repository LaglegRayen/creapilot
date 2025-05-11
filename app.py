import os
from flask import Flask, render_template
from dotenv import load_dotenv
from blueprints.video_ideas import bp as video_ideas_bp
from blueprints.transcript_analyzer import bp as transcript_bp
from blueprints.hashtag_assistant import bp as hashtag_bp


load_dotenv()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')

    # Register blueprints
    # Import blueprints for each core feature:
    # - Video idea generator: Generates content ideas based on topic/niche
    # - Transcript analyzer: Analyzes video transcripts for insights
    # - Hashtag assistant: Generates platform-specific hashtags


    # Register blueprints with URL prefixes to create API endpoints
    # Each blueprint handles its own routes, templates and logic
    app.register_blueprint(video_ideas_bp, url_prefix='/api/video_ideas')
    app.register_blueprint(transcript_bp, url_prefix='/api/transcript_analyzer')
    app.register_blueprint(hashtag_bp, url_prefix='/api/hashtags')

    register_error_handlers(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app

def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(e):
        return {'error': 'Bad Request'}, 400

    @app.errorhandler(404)
    def not_found(e):
        return {'error': 'Not Found'}, 404

    @app.errorhandler(500)
    def internal_error(e):
        return {'error': 'Internal Server Error'}, 500

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) 