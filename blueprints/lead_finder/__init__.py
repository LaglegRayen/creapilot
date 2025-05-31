from flask import Blueprint

bp = Blueprint('lead_finder', __name__)

from . import routes 