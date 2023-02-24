from . import callback_blu
from flask import request, jsonify
from utils.Yaml import *
import random
import datetime


@callback_blu.route('/', methods=['GET', 'POST'])
def index():
    return "OK"


@callback_blu.route('/get/sentence', methods=['GET', 'POST'])
def get_sentence():
    types = "interesting"
    if request.method == "GET":
        kind = types
    else:
        request_data = request.get_json()
        kind = request_data.get('type')
    t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text = Yaml().get_yaml_data("wordlist.yaml")
    sentence = random.choice(text[kind])
    res = {"code": 200, "type": kind, "content": sentence, "time": t}
    return jsonify(res)




