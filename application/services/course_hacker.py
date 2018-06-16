import asyncio
import requests
from bs4 import BeautifulSoup
from datetime import datetime
# BUILD YOUR OWN
CAPTCHA_SERVER = ''
# 选课服务器
HOST = 'http://xk.shu.edu.cn:8080'
# 学号
ID = ''
# 密码
PASSWORD = ''
# 课程列表，no 代表课程号 class 代表教师号 [{'no': '06266077', 'class': '1000'}]
COURSES = [{'no': '06266077', 'class': '1000'}]
# 请求数量 15 已经够了
NUM_OF_REQS = 15 

def get_proxies():
    return None


def captcha_solver(im, im_type=3040, timeout=60, site=''):
    endpoint = '/jwc'
    files = {'captcha': ('captcha.jpg', im)}
    r = requests.post(CAPTCHA_SERVER + endpoint,
                      files=files, proxies=get_proxies())
    return {'Result': r.json()['result']}


class XK():
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    def __init__(self, card_id, password, host='http://xk.shu.edu.cn:8080'):
        self.card_id = card_id
        self.password = password
        self.site = ''
        self.subject = ''
        self.session = requests.Session()
        self.data = ''
        self.host = host
        self.mode = None

    def login(self):
        r = self.session.get(
            self.host + '/Login/GetValidateCode?GetTimestamp()', timeout=10, stream=True, proxies=get_proxies())
        self.captcha = captcha_solver(
            r.raw.read(), site='XK')['Result']
        post_data = {
            'txtUserName': self.card_id,
            'txtPassword': self.password,
            'txtValiCode': self.captcha}
        r = self.session.post(self.host + '/',
                              data=post_data, headers=self.headers, timeout=60, proxies=get_proxies())
        return r.text.find('首页') != -1

    def logout(self):
        self.session.get(self.host + '/Login/Logout',
                         proxies=get_proxies())

    def enter_fast_input(self):
        self.session.get(self.host + '/CourseSelectionStudent/FastInput')
        self.mode = 'fastinput'

    def select_courses(self, courses):
        if self.mode != 'fastinput':
            self.enter_fast_input()
        data = {'IgnorClassMark': 'False',
                'IgnorCourseGroup': 'False',
                'IgnorCredit': 'False',
                'StudentNo': self.card_id
                }
        failed_names = ('no', 'name', 'class', 'teacher', 'credit',
                        'time', 'place', 'campus', 'notice')
        success_names = ('no', 'name', 'class', 'teacher', 'credit',
                         'time', 'place', 'campus')
        for i in range(len(courses)):
            data['ListCourse[' + str(i) + '].CID'] = courses[i]['no']
            data['ListCourse[' + str(i) + '].TNo'] = courses[i]['class']
            data['ListCourse[' + str(i) + '].NeedBook'] = 'false'
        r = self.session.post(
            self.host + '/CourseSelectionStudent/CtrlViewOperationResult', data=data)
        assert r.text.find('验证码') == -1
        soup = BeautifulSoup(r.text, "html.parser")
        tables = soup.findAll('table')
        success_courses = []
        failed_courses = []
        for table in tables:
            rows = table.findAll('tr')
            success = rows[0].td.get_text(strip=True) == '选课成功课程'
            for row in rows[2:]:
                cells = row.findAll("td")
                if success:
                    course = {
                        success_names[key]: cell.get_text(strip=True) for (key, cell) in enumerate(cells[1:])
                    }
                    success_courses.append(course)
                else:
                    course = {
                        failed_names[key]: cell.get_text(strip=True) for (key, cell) in enumerate(cells[1:])
                    }
                    failed_courses.append(course)
        return {'success_courses': success_courses, 'failed_courses': failed_courses}


async def hack(no, watch=False):
    print("init object", no)
    await asyncio.sleep(no)
    xk = XK(ID, PASSWORD, host=HOST)
    loop = asyncio.get_event_loop()
    future = loop.run_in_executor(None, xk.login)
    response = await future
    print(response)
    while True:
        try:
            print('start request', no)
            future = loop.run_in_executor(None, xk.select_courses, COURSES)
            if watch:
                response = await future
                print(response)
                print('response recieve, sleeping', no)
            await asyncio.sleep(10)
        except:
            future = loop.run_in_executor(None, xk.login)
            response = await future
            print('login expired, relogin', _, response)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    for no in range(NUM_OF_REQS):
        asyncio.ensure_future(hack(no, watch=True))
    try:
        loop.run_forever()
    finally:
        loop.close()
