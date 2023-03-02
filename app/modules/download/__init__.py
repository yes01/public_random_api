from flask import Blueprint

download_blu = Blueprint("download", __name__)

from . import views