import os
from flask import Flask, render_template
from dotenv import load_dotenv
from blueprints.social_scraper import bp as social_scraper_bp
from blueprints.lead_finder import bp as lead_finder_bp
from blueprints.product_research import bp as product_research_bp
from blueprints.sql_assistant import bp as sql_assistant_bp

load_dotenv()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')

    # Register blueprints
    app.register_blueprint(social_scraper_bp, url_prefix='/api/social')
    app.register_blueprint(lead_finder_bp, url_prefix='/api/leads')
    app.register_blueprint(product_research_bp, url_prefix='/api/products')
    app.register_blueprint(sql_assistant_bp, url_prefix='/api/sql')

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