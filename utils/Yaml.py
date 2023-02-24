import os
import yaml


class Yaml:

    @staticmethod
    def get_yaml_data(yaml_file):
        path = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0] + "/tools/"
        yaml_path = os.path.join(path, yaml_file)
        file = open(yaml_path, 'r', encoding="utf-8")
        file_data = file.read()
        file.close()
        data = yaml.load(file_data, Loader=yaml.FullLoader)

        return data
