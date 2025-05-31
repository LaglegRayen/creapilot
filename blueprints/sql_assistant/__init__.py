from flask import Blueprint

bp = Blueprint('sql_assistant', __name__)

from . import routes 