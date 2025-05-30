from flask import Flask

def create_app():
    app = Flask(__name__)

    # Configuration settings can be added here
    app.config['DEBUG'] = True  # Set to False in production

    # Import and register blueprints or routes here if needed

    return app

app = create_app()