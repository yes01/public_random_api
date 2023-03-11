from . import live_source_blu
from flask import redirect, send_from_directory
from utils.huya import *
from utils.douyu import *
from utils.douyin import *
from utils.bilibili import *
import os

directory = os.path.split(os.path.split(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0])[0])[0] + \
                "/static/"


@live_source_blu.route('/live/huya/<rid>', methods=['GET'])
def hu_ya(rid):
    url = HuYa(rid, 1463993859134, 1).get_real_url()
    if len(url) != 0:
        real_url = url[0]
        return redirect(real_url)
    else:
        return send_from_directory(directory, 'zanweikaibo.jpg', as_attachment=False)


@live_source_blu.route('/live/douyu/<rid>', methods=['GET'])
def dou_yu(rid):
    url = DouYu(rid).get_real_url()
    if len(url) != 0:
        real_url = url["flv"]
        return redirect(real_url)
    else:
        return send_from_directory(directory, 'zanweikaibo.jpg', as_attachment=False)


@live_source_blu.route('/live/douyin/<rid>', methods=['GET'])
def dou_yin(rid):
    url = DouYin(rid).get_real_url()
    if len(url) != 0:
        real_url = url["douyin"][0]["flv_FULL_HD1"]
        return redirect(real_url)
    else:
        return send_from_directory(directory, 'zanweikaibo.jpg', as_attachment=False)


@live_source_blu.route('/live/bilibili/<rid>', methods=['GET'])
def bilibili(rid):
    url = BiliBili(rid).get_real_url()
    if len(url) != 0:
        real_url = url["bili"][0]["线路1_10000"]
        return redirect(real_url)
    else:
        return send_from_directory(directory, 'zanweikaibo.jpg', as_attachment=False)
