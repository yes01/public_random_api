import requests
import time
import os
from multiprocessing import Pool

path = (os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]) + "/static/IPTV/"


def get(url, GetStatus=0):
    headers = {
        'Accept-Language': "zh-CN,zh",
        'User-Agent': "Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36",
        'Accept-Encoding': "gzip"
    }
    try:
        res = requests.request("GET", url, headers=headers, timeout=2)  # 此处设置超时时间
    except:
        return 0
    if GetStatus == 1:
        return res.status_code
    else:
        if res.status_code == 200:
            res = str(res.content, 'utf-8')
        else:
            res = 0
        return res


def checkLink(url):
    res = get(url, 1)
    if res == 200:
        return 1
    else:
        return 0


def displayMsg(workname='Default', msg=''):
    now = time.asctime(time.localtime(time.time()))
    print(f'{now} - {workname}: ' + msg)


def writeFile(filename, content):
    with open(filename, 'w', encoding='utf8') as file:
        file.write(content)


def endWith(fileName, *endstring):
    array = map(fileName.endswith, endstring)
    if True in array:
        return True
    else:
        return False


def m3u_filelist(path):
    fileList = os.listdir(path)
    files = []
    for filename in fileList:
        if endWith(filename, '.m3u8'):
            files.append(filename)  # 所有m3u8文件列表
    return files


def m3u8_load(m3uFile):
    channel = {}
    errorNum = 0
    status = 0  # 实时改变步骤状态
    with open(m3uFile, 'r', encoding='utf8') as file:
        displayMsg('m3u8_load', f'当前载入列表：{m3uFile}')
        for line in file:
            # 如果当前是描述行：
            if line.startswith('#EXTINF:-1'):
                if status != 0:
                    displayMsg('m3u8_load', f'{m3uFile}当前列表缺少行')
                    errorNum += 1
                    exit()
                channelInfo = str(line).replace('\n', '')
                status = 1

            # 如果当前是URL行
            if line.startswith('http') or line.startswith('rtsp') or line.startswith('https'):  # 当前行为URL
                if status != 1:
                    displayMsg('m3u8_load', f'{m3uFile}当前列表缺少行')
                    errorNum += 1
                    exit()
                channel[channelInfo] = str(line).replace('\n', '')
                status = 2
            # 上述判断完成
            if status == 2:  # 上述步骤处理完毕
                status = 0
        displayMsg('m3u8_load', f'{m3uFile} 解析完毕')
        return channel


def work(m3u_data, outputFile, workname='Default'):
    print(m3u_data)
    for data in m3u_data:
        print(data)
        txt1 = data.split(',')  # 分割节目名称与标签属性
        name = txt1[1]  # 电视名称
        url = m3u_data[data]  # 播放链接
        with open(outputFile, 'a', encoding='utf8') as file:
            file.write(data + '\n')
            file.write(url + '\n')
        # if checkLink(url):
        #     displayMsg(workname, f'{name} 访问成功')
        #     with open(outputFile, 'a', encoding='utf8') as file:
        #         file.write(data + '\n')
        #         file.write(url + '\n')
        # else:
        #     displayMsg(workname, f'{name} 【失败】！')


if __name__ == '__main__':
    outputFile = path + 'checkOutput.m3u8'
    displayMsg('Master', '开始读取文件列表：')
    fileList = m3u_filelist(os.getcwd())
    # if outputFile in fileList:  # 除去输出文件本身
    #     fileList.remove(outputFile)

    writeFile(outputFile, '#EXTM3U\n')

    p = Pool(4)
    for file in fileList:
        p.apply_async(work, args=(m3u8_load(file), outputFile, file))
    p.close()
    p.join()
