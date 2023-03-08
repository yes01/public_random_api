from flask import Blueprint

live_source_blu = Blueprint("live_source", __name__)

from . import views