from flask import Blueprint

bp = Blueprint('social_scraper', __name__)

from . import routes 