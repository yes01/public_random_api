from flask import Blueprint

callback_blu = Blueprint("callback", __name__)

from . import views