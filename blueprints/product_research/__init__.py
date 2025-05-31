from flask import Blueprint

bp = Blueprint('product_research', __name__)

from . import routes 