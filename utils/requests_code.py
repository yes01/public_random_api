import requests


def requests_get_code(real_dict):
    for real_ in real_dict:
        try:
            code = requests.get(real_dict[real_], stream=True, timeout=1).status_code
            if code == 200:
                return real_dict
        except Exception as e:
            print(e)
