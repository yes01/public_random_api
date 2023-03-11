import os
import time
import yaml


class Yaml:

    @staticmethod
    def display_msg(work_name='Default', msg=''):
        now = time.asctime(time.localtime(time.time()))
        print(f'{now} - {work_name}: ' + msg)

    @staticmethod
    def get_yaml_data(yaml_file):
        path = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0] + "/tools/"
        yaml_path = os.path.join(path, yaml_file)
        file = open(yaml_path, 'r', encoding="utf-8")
        file_data = file.read()
        file.close()
        data = yaml.load(file_data, Loader=yaml.FullLoader)

        return data

    @staticmethod
    def write_yaml(yaml_file, data):
        path = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0] + "/tools/"
        yaml_path = os.path.join(path, yaml_file)
        with open(yaml_path, encoding="utf-8", mode="w") as f:
            yaml.dump(data, stream=f, allow_unicode=True)

    @staticmethod
    def write_file(filename, content):
        with open(filename, 'w', encoding='utf8') as file:
            file.write(content)

    def write_m3u8(self, out_put_file, data):
        with open(out_put_file, 'a', encoding='utf8') as file:
            for line in data:
                file.write(line)
            self.display_msg('写入直播源到{}文件'.format(out_put_file), '成功！！！')
