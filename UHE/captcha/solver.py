"""
temporary using http://www.ruokuai.com captcha solver api
replace it later
"""
import requests

class Solver():
    def __init__(self):
        pass
    def init_app(self,app):
        self.username=app.config["CAPTCHA_SOLVER_USERNAME"]
        self.password=app.config["CAPTCHA_SOLVER_PASSWORD"]
        self.soft_id=app.config["CAPTCHA_SOLVER_SOFTID"]
        self.soft_key=app.config["CAPTCHA_SOLVER_SOFTKEY"]
        self.base_params = {
            'username': self.username,
            'password': self.password,
            'softid': self.soft_id,
            'softkey': self.soft_key,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'User-Agent': 'ben',
        }
    def create(self, im,im_type=3040, timeout=60,site=''):
        params = {
            'typeid': im_type,
            'timeout': timeout,
        }
        params.update(self.base_params)
        files = {'image': ('a.jpg', im)}
        r = requests.post('http://api.ruokuai.com/create.json',
                          data=params, files=files)
        return r.json()

    def report_error(self, im_id):
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://api.ruokuai.com/reporterror.json',
                          data=params, headers=self.headers)
        return r.json()
