from . import download_blu
import os
from flask import send_from_directory


@download_blu.route('/download/<file>', methods=['GET'])
def download(file):
    path = os.path.split(os.path.split(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0])[0])[0] + \
           "/static/IPTV/"
    return send_from_directory(path, '{}.m3u8'.format(file), as_attachment=True)
