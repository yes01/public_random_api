from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
from utils.Yaml import *
from utils.huya import *
from utils.douyu import *
from utils.douyin import *
from utils.bilibili import *

yaml = Yaml()
default_url = "https://flask.jiaotailang.online/live/"


class Reptile:

    @staticmethod
    def display_msg(work_name='Default', msg=''):
        now = time.asctime(time.localtime(time.time()))
        print(f'{now} - {work_name}: ' + msg)

    @staticmethod
    def get_url(address):
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
        }
        res = requests.get(address, headers=headers)
        return res

    def get_dou_yu_sort(self):
        link_dict = {}
        res = self.get_url("https://www.douyu.com/directory/all")
        compile_text = re.compile('<div class="Aside-menu">(.*?)\n').findall(res.text)[0]
        all_items = re.compile('<div class="Aside-menu-list">(.*?)</div>').findall(compile_text)
        for item in all_items:
            htmls = pq(item)
            links = htmls('a').items()
            for link in links:
                link_dict[link.text()] = 'https://www.douyu.com' + link.attr('href')
        return link_dict

    def get_dou_yu_content(self, live_type_url='https://www.douyu.com/g_wzry', heat=60):
        """
        获取斗鱼网址指定「热度」的主播相关内容
        heat: 热度
        """
        rid_list = []
        rid_lists = []
        title_name_list = []
        title_name_lists = []
        dou_yu_dict = []
        response = self.get_url(live_type_url)
        pages = eval(re.compile('"pageCount":(.*?),').findall(response.text)[0])
        print('共有' + str(pages) + '页,正在爬取第1页')
        htmls = pq(response.text)
        items = htmls('#listAll > div.layout-Module-container.layout-Cover.ListContent > ul>li').items()
        for item in items:
            rid = item('div > a.DyListCover-wrap').attr('href')
            game = item('div > a.DyListCover-wrap > div.DyListCover-content > div:nth-child(1) > span').text()
            anchor = item('div > a.DyListCover-wrap > div.DyListCover-content > div:nth-child(2) > h2').text()
            hot = item('div > a.DyListCover-wrap > div.DyListCover-content > div:nth-child(2) > span').text()
            numbers = re.findall(r'\d+', hot)
            if "万" in str(hot) and int(numbers[0]) >= heat and rid[1:].isdigit():
                self.display_msg('爬取「{0}」-「{1}」主播房间号：'.format(game, anchor), '{}'.format(rid[1:]))
                title_name = '「{}」'.format(game) + '{}'.format(anchor) + "「{}🔥」".format(hot)
                title_name_list.append(title_name)
                rid_list.append(rid[1:])
                dou_yu_dict = {rid_list[i]: title_name_list[i] for i in range(len(rid_list))}
        return dou_yu_dict
        # if pages == 1:
        #     print('爬取结束')
        #     return
        # ids = re.compile('"tabTagPath":"/gapi/rkc/directory/c_tag/(.*?)/list",').findall(response.text)[0]
        # for i in range(1, pages):
        #     print('正在爬取第' + str(i + 1) + '页')
        #     url = 'https://www.douyu.com/gapi/rkc/directory/' + ids + '/' + str(i + 1)
        #     rsp = self.get_url(url)
        #     json_text = json.loads(rsp.text)
        #     datas = json_text['data']['rl']
        #     for data in datas:
        #         hot = data['ol']
        #         if hot < 10000:
        #             hot = str(hot)
        #         else:
        #             hot = str(int(hot / 1000))
        #             if hot[-1] == '0':
        #                 hot = hot[0] + '万'
        #             else:
        #                 hot = hot[0] + '.' + hot[1] + '万'
        #         rid = str(data['rid'])
        #         game = data['c2name']
        #         anchor = data['nn']
        #         hot = hot
        #         numbers = re.findall(r'\d+', hot)
        #         if "万" in str(hot) and int(numbers[0]) >= heat:
        #             title_name = '「{}」'.format(game) + '{}'.format(anchor) + "「{}🔥」".format(hot)
        #             title_name_lists.append(title_name)
        #             rid_lists.append(rid)
        #             dou_yu_dicts = {rid_lists[i]: title_name_lists[i] for i in range(len(rid_lists))}
        #         dou_yu_dicts.update(dou_yu_dict)
        #         print(dou_yu_dicts)

    def save_dou_yu_yaml(self):
        dou_yu_dicts = {}
        link_dict = self.get_dou_yu_sort()
        for key, value in link_dict.items():
            dou_yu_dict = self.get_dou_yu_content(live_type_url=value)
            dou_yu_dicts.update(dou_yu_dict)
        yaml.write_yaml("reptile_douyu.yaml", dou_yu_dicts)
        self.display_msg('爬取内容写入「{}」文件：'.format("reptile_douyu.yaml"), '成功！！！')

    def write_dou_yu_m3u8(self, filename='douyu.m3u8'):
        """
        根据reptile_douyu.yaml文件内容，获取真实直播流并写入到filename
        :param filename: 存储文件名称
        """
        data = yaml.get_yaml_data("reptile_douyu.yaml")
        datas = []
        for key, value in data.items():
            flask_url = default_url + "douyu/" + key
            self.display_msg('获取斗鱼{}直播流：'.format(value), '{}'.format(flask_url))
            txt = '#EXTINF:-1 tvg-logo="" group-title="斗鱼", {}'.format(value)
            datas.append(txt + '\n')
            datas.append(flask_url + '\n')
            # url = DouYu(key).get_real_url()
            # self.display_msg('获取斗鱼{}直播流：'.format(value), '{}'.format(url))
            # if len(url) != 0:
            #     real_url = url["flv"]
            #     txt = '#EXTINF:-1 tvg-logo="" group-title="斗鱼", {}'.format(value)
            #     datas.append(txt + '\n')
            #     datas.append(real_url + '\n')
        yaml.write_file(filename, '#EXTM3U\n')
        yaml.write_m3u8(filename, datas)

    def get_hu_ya_content(self, heat=60):
        """
        获取虎牙网址指定「热度」的主播相关内容，写入到/tools/reptile_huya.yaml文件
        heat: 热度
        """
        urls = []
        rid_list = []
        title_name_list = []
        res = self.get_url("https://www.huya.com/g")
        res.raise_for_status()
        res.encoding = res.apparent_encoding
        htmls = BeautifulSoup(res.text, 'html.parser')
        contents = htmls.find_all('a', class_='recomend-item j_sidebar-recomend-item')
        for i in contents:
            href = i['href']
            title = i['title']
            urls.append([href, title])
        for url in urls:
            r = self.get_url(url[0])
            htmls = BeautifulSoup(r.text, 'html.parser')
            a = htmls.find_all('li', class_='game-live-item')
            for i in a:
                num = i.select('i', class_='js-num')[3].text
                title = i.select('img')[0]['alt']
                href = i.select('a')[1]['href']
                title1 = i.select('a')[1]['title']
                numbers = re.findall(r'\d+', num)
                if len(numbers) != 0 and int(numbers[0]) >= heat and "重播" not in title1:
                    self.display_msg('爬取「{0}」-「{1}」主播房间号：'.format(url[1], title[:-3]), '{}'.format(href[21:]))
                    title_name = "「{}」".format(url[1]) + title[:-3] + "「{}🔥」".format(num)
                    title_name_list.append(title_name)
                    rid_list.append(href[21:])
        hu_ya_dict = {rid_list[i]: title_name_list[i] for i in range(len(rid_list))}
        yaml.write_yaml("reptile_huya.yaml", hu_ya_dict)
        self.display_msg('爬取内容写入「{}」文件：'.format("reptile_huya.yaml"), '成功！！！')

    def write_bilibili_m3u8(self, filename='bilibili.m3u8'):
        """
        根据reptile_bilibili.yaml文件内容，获取真实直播流并写入到filename
        :param filename: 存储文件名称
        """
        data = yaml.get_yaml_data("reptile_bilibili.yaml")
        datas = []
        for key, value in data.items():
            flask_url = default_url + "bilibili/" + key
            self.display_msg('获取bilibili{}直播流：'.format(value), '{}'.format(flask_url))
            txt = '#EXTINF:-1 tvg-logo="" group-title="B站", {}'.format(value)
            datas.append(txt + '\n')
            datas.append(flask_url + '\n')
            # url = BiliBili(key).get_real_url()
            # self.display_msg('获取bilibili{}直播流：'.format(value), '{}'.format(url))
            # if len(url) != 0:
            #     real_url = url["bili"][0]["线路1_10000"]
            #     txt = '#EXTINF:-1 tvg-logo="" group-title="B站", {}'.format(value)
            #     datas.append(txt + '\n')
            #     datas.append(real_url + '\n')
        yaml.write_file(filename, '#EXTM3U\n')
        yaml.write_m3u8(filename, datas)

    def write_hu_ya_m3u8(self, filename='huya.m3u8'):
        """
        根据reptile_huya.yaml文件内容，获取真实直播流并写入到filename
        :param filename: 存储文件名称
        """
        data = yaml.get_yaml_data("reptile_huya.yaml")
        datas = []
        for key, value in data.items():
            flask_url = default_url + "huya/" + key
            self.display_msg('获取虎牙{}直播流：'.format(value), '{}'.format(flask_url))
            txt = '#EXTINF:-1 tvg-logo="" group-title="虎牙", {}'.format(value)
            datas.append(txt + '\n')
            datas.append(flask_url + '\n')
            # url = HuYa(key, 1463993859134, 1).get_real_url()
            # self.display_msg('获取虎牙{}直播流：'.format(value), '{}'.format(url))
            # if len(url) != 0:
            #     real_url = url[0]
            #     txt = '#EXTINF:-1 tvg-logo="" group-title="虎牙", {}'.format(value)
            #     datas.append(txt + '\n')
            #     datas.append(real_url + '\n')
        yaml.write_file(filename, '#EXTM3U\n')
        yaml.write_m3u8(filename, datas)

    def write_dou_yin_m3u8(self, filename='douyin.m3u8'):
        """
        根据reptile_douyin.yaml文件内容，获取真实直播流并写入到filename
        :param filename: 存储文件名称
        """
        data = yaml.get_yaml_data("reptile_douyin.yaml")
        datas = []
        for key, value in data.items():
            flask_url = default_url + "douyin/" + key
            self.display_msg('获取抖音{}直播流：'.format(value), '{}'.format(flask_url))
            txt = '#EXTINF:-1 tvg-logo="" group-title="抖音", {}'.format(value)
            datas.append(txt + '\n')
            datas.append(flask_url + '\n')
            # url = DouYin(key).get_real_url()
            # if len(url) != 0:
            #     real_url = url["douyin"][0]["flv_FULL_HD1"]
            #     self.display_msg('获取抖音「{}」直播流：'.format(value), '{}'.format(real_url))
            #     txt = '#EXTINF:-1 tvg-logo="" group-title="抖音", {}'.format(value)
            #     datas.append(txt + '\n')
            #     datas.append(real_url + '\n')
        yaml.write_file(filename, '#EXTM3U\n')
        yaml.write_m3u8(filename, datas)
