"""
example http://www.ruokuai.com captcha solver api
replace it later
"""
import requests
from flask import current_app


def get_proxies():
    proxies = {
        'http': current_app.config['PROXY'],
        'https': current_app.config['PROXY']
    }
    return None


class Solver:
    def __init__(self):
        pass

    def init_app(self, app):
        pass
        # self.username = app.config["CAPTCHA_SOLVER_USERNAME"]
        # self.password = app.config["CAPTCHA_SOLVER_PASSWORD"]
        # self.soft_id = app.config["CAPTCHA_SOLVER_SOFTID"]
        # self.soft_key = app.config["CAPTCHA_SOLVER_SOFTKEY"]
        # self.base_params = {
        #     'username': self.username,
        #     'password': self.password,
        #     'softid': self.soft_id,
        #     'softkey': self.soft_key,
        # }
        # self.headers = {
        #     'Connection': 'Keep-Alive',
        #     'Expect': '100-continue',
        #     'User-Agent': 'ben',
        # }

    def create(self, im, im_type=3040, timeout=60, site=''):
        if site == 'XK' or site == 'CJ':
            endpoint = 'jwc'
        elif site == 'phylab':
            endpoint = 'phylab'
        else:
            params = {
                'typeid': im_type,
                'timeout': timeout,
            }
            params.update(self.base_params)
            files = {'image': ('a.jpg', im)}
            r = requests.post('http://api.ruokuai.com/create.json',
                              data=params, files=files)
            return r.json()
        params = {
            'typeid': im_type,
            'timeout': timeout,
        }
        params.update(self.base_params)
        files = {'captcha': ('captcha.jpg', im)}
        r = requests.post(current_app.config['CAPTCHA_SERVER'] + endpoint,
                          data=params, files=files, proxies=get_proxies())
        return {'Result': r.json()['result']}

    def report_error(self, im_id):
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://api.ruokuai.com/reporterror.json',
                          data=params, headers=self.headers)
        return r.json()
