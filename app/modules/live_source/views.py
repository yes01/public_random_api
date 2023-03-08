from . import live_source_blu
from utils.huya import *
from utils.douyu import *
from utils.douyin import *


@live_source_blu.route('/live/huya/<rid>', methods=['GET'])
def hu_ya(rid):
    url = HuYa(rid, 1463993859134, 1).get_real_url()
    real_url = url[0]
    if real_url is not None:
        return real_url
    else:
        return 'the broadcast is not started or the live room does not exist'


@live_source_blu.route('/live/douyu/<rid>', methods=['GET'])
def dou_yu(rid):
    url = DouYu(rid).get_real_url()
    real_url = url["flv"]
    if real_url is not None:
        return real_url
    else:
        return 'the broadcast is not started or the live room does not exist'


@live_source_blu.route('/live/douyin/<rid>', methods=['GET'])
def dou_yin(rid):
    url = DouYin(rid).get_real_url()
    real_url = url["douyin"][0]["flv_FULL_HD1"]
    if real_url is not None:
        return real_url
    else:
        return 'the broadcast is not started or the live room does not exist'
