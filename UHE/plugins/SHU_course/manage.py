import datetime
import re
import time

import requests
from bs4 import BeautifulSoup
from flask import current_app
from flask_admin.contrib.mongoengine import ModelView
from mongoengine.context_managers import switch_collection
from UHE.admin.views import BasicPrivateModelView
from UHE.calendar.models import Activity, Event
from UHE.extensions import admin, captcha_solver, celery, db
from UHE.plugins import UHEPlugin
from UHE.plugins.SHU_api import get_courses
from .models import Course, CourseOfTerm, Teacher


def get_xk(url):
    term = get_term(url)
    courselist = get_latest_course(url)
    save_courses(courselist, term)


def get_teacher(url, no):
    convert = {
        '姓名:': 'name',
        '性别:': 'sex',
        '学历:': 'education',
        '学位:': 'degree',
        '职称:': 'title',
        '部门:': 'dept',
        '工号:': 'no',
        '自我简介': 'intro'
    }
    p_url = url + str(no)
    r = requests.get(p_url)
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.table
    if table is None:
        return
    teacher = {}
    tds = iter(table.find_all('td'))
    for td in tds:
        text = td.text.strip()
        if text in convert.keys():
            td = next(tds)
            key = convert[text]
            teacher[key] = td.text.strip()
    teacher = Teacher(**teacher)
    print('saving', teacher)
    teacher.save()


def get_teachers():
    url = 'http://jwc.shu.edu.cn:8080/jwc/tinfo/viewinfo1.jsp?tid='
    for no in range(10000000, 10010620):
        print('getting no:', no)
        get_teacher(url, no)
    for no in range(51000000, 51005000):
        print('getting no:', no)
        get_teacher(url, no)
    for no in range(31000000, 31005000):
        print('getting no:', no)
        get_teacher(url, no)
    for no in range(61000000, 61005000):
        print('getting no:', no)
        get_teacher(url, no)


def save_courses(courselist, term):
    term_string = current_app.school_time.term_string
    for course in courselist:
        course_basic = {
            key: course.get(key) for key in ('no', 'name', 'teacher', 'credit', 'school', 'tag')
        }
        teacher_name = course['teacher_name']
        teacher_no = course['teacher_id']
        if teacher_no is not None:
            teacher = Teacher.objects(no=teacher_no).first()
            if teacher is None:
                get_teacher(
                    'http://jwc.shu.edu.cn:8080/jwc/tinfo/viewinfo1.jsp?tid=', teacher_no)
                teacher = Teacher.objects(no=teacher_no).first()      
        else:
            teacher = Teacher.objects(name=teacher_name).first()
            if teacher is None:
                if teacher_name[-1] == '等':
                    teacher = Teacher.objects(name=teacher_name[:-1]).first()
        assert teacher is not None
        course_basic['teacher'] = teacher
        course_db = Course.objects(
            no=course['no'], teacher=teacher).first()
        if course_db is None:
            course_db = Course(**course_basic)
            course_db.save()
        if term not in course_db.terms:
            course_db.terms.append(term)
            course_db.save()
        course_detail = {
            key: course.get(key) for key in ('course', 'q_time', 'q_place', 'teacher_no', 'time', 'place', 'capacity', 'enroll', 'campus')
        }
        course_detail['course'] = course_db
        course_detail['course_no'] = course_db.no
        course_detail['course_name'] = course_db.name
        course_detail['term'] = term
        course_detail['credit'] = course_db.credit
        course_detail['teacher'] = teacher
        course_detail['teacher_name'] = teacher.name
        course_of_term_db = CourseOfTerm.objects(
            course=course_db, teacher_no=course['teacher_no']).update(**course_detail)
        if not course_of_term_db:
            course_of_term_db = CourseOfTerm(**course_detail)
            course_of_term_db.save()


TERM_INT = {
    '秋': 1,
    '冬': 2,
    '春': 3,
    '夏': 4
}

QUERY_DATA = {
    'CourseNo': '',
    'CourseName': '',
    'TeachNo': '',
    'TeachName': '',
    'CourseTime': '',
    'NotFull': 'false',
    'Credit': '',
    'Campus': '0',
    'Enrolls': '',
    'DataCount': '0',
    'MinCapacity': '',
    'MaxCapacity': '',
    'PageIndex': '1',
    'PageSize': '4000',
    'FunctionString': 'InitPage'
}
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,th;q=0.2,zh-TW;q=0.2',
    'Cache-Control': 'max-age=0',
    'Host': 'xk.shu.edu.cn:8080',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
}


# @celery.task()
def get_term(url):
    s = requests.Session()
    print('start get url')
    num = 3
    while num > 0:
        try:
            print('pending')
            result = s.get(url, timeout=3, headers=HEADERS)
            assert result.status_code == 200
        except Exception as e:
            print('error, try again', e)
            num -= 1
            time.sleep(5)
        else:
            break
    else:
        print('Try 3 times, But all failed')
        assert False
    info = re.search(
        r'(\d{4})-(\d{4})学年([\u4e00-\u9fa5])季学期', result.text, flags=0).groups()
    print(info)
    year = int(info[0])
    term = TERM_INT[info[2]]
    # term = info[2]
    print(year, term)
    return '{}_{}'.format(year, term)


def get_latest_course(url):
    print('getting data from {}'.format(url))
    courselist = []
    success = False
    maxtry = 10
    while not success and maxtry != 0:
        maxtry = maxtry - 1
        print('tring to get captcha {}, try left'.format(maxtry))
        s = requests.Session()
        r = s.get(
            url + 'Login/GetValidateCode?%20%20+%20GetTimestamp()', timeout=10, stream=True)
        captcha_img = r.raw.read()
        checkimg = captcha_solver.create(captcha_img, site='xk')
        print('get checkimg success', checkimg)
        postData = {
            'txtUserName': current_app.config['TESTING_CARD_ID'],
            'txtPassword': current_app.config['TESTING_PASSWORD'],
            'txtValiCode': checkimg['Result'],
        }
        r = s.post(url, data=postData, timeout=10)
        if r.text.find('验证码错误') != -1:
            continue
        elif r.text.find('首页') != -1:
            print('登陆成功')
            time.sleep(3)
            r = s.get(url + 'StudentQuery/QueryCourse')
            time.sleep(3)
            r = s.post(url + 'StudentQuery/CtrlViewQueryCourse',
                       data=QUERY_DATA)
            time.sleep(3)
            s.get(url + 'Login/Logout')
            success = True
            print('login successful')
        else:
            continue
    assert maxtry != 0
    assert success
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table")
    row = table.findAll("tr")
    for row in table.findAll("tr"):
        cells = row.findAll("td")
        if len(cells) == 13:
            courseno = cells[0].get_text(strip=True)
            coursename = cells[1].get_text(strip=True)
            credit = cells[2].get_text(strip=True)
            teachno = cells[3].get_text(strip=True)
            teachid = cells[4].get('onclick')
            if teachid is not None:
                teachid = teachid[-10:-2]
            teachname = cells[4].get_text(strip=True)
            coursetime = cells[5].get_text(strip=True)
            courseplace = cells[6].get_text(strip=True)
            capacity = cells[7].get_text(strip=True)
            enroll = cells[8].get_text(strip=True)
            campus = cells[9].get_text(strip=True)
            restrict = cells[10].get_text(strip=True)
            qtime = cells[11].get_text(strip=True)
            qplace = cells[12].get_text(strip=True)
        elif len(cells) == 10:
            teachno = cells[0].get_text(strip=True)
            teachid = cells[1].get('onclick')
            if teachid is not None:
                teachid = teachid[-10:-2]
            teachname = cells[1].get_text(strip=True)
            coursetime = cells[2].get_text(strip=True)
            courseplace = cells[3].get_text(strip=True)
            capacity = cells[4].get_text(strip=True)
            enroll = cells[5].get_text(strip=True)
            campus = cells[6].get_text(strip=True)
            restrict = cells[7].get_text(strip=True)
            qtime = cells[8].get_text(strip=True)
            qplace = cells[9].get_text(strip=True)
        if len(cells) == 13 or len(cells) == 10:
            school, tag = get_college_and_tag(courseno)
            course = {
                'no': courseno,
                'name': coursename,
                'credit': credit,
                'teacher_no': teachno,
                'teacher_id': teachid,
                'teacher_name': teachname,
                'time': coursetime,
                'place': courseplace,
                'capacity': capacity,
                'enroll': enroll,
                'campus': campus,
                'restrict': restrict,
                'q_time': qtime,
                'q_place': qplace,
                'school': school,
                'tag': [tag]
            }
            courselist.append(course)
    return courselist


def get_college_and_tag(courseid):
    x1 = courseid[0:2]
    x2 = courseid[2:4]
    x3 = courseid[4]
    x4 = courseid[5]
    if x1 == '00':
        college = '特殊'
    elif x1 == '01':
        college = '理学院'
    elif x1 == '02':
        if (x2 == '09') | (x2 == '75'):
            college = '社会学院'
        else:
            college = '文学院'
    elif x1 == '03':
        college = '外国语学院'
    elif x1 == '04':
        if x2 == '10':
            college = '图书情报档案系'
        elif x2 == '13' or x2 == '14'or x2 == '15':
            college = '经济学院'
        else:
            college = '管理学院'
    elif x1 == '06':
        college = '法学院'
    elif x1 == '07':
        college = '通信与信息工程学院'
    elif x1 == '08':
        college = '计算机工程与科学学院'
    elif x1 == '09':
        college = '机电工程与自动化学院'
    elif x1 == '10':
        college = '材料科学与工程学院'
    elif x1 == '11':
        college = '环境与化学工程学院'
    elif x1 == '12':
        college = '生命科学学院'
    elif x1 == '13':
        college = '美术学院'
    elif x1 == '14':
        college = '上海电影学院'
    elif x1 == '15':
        college = '悉尼工商学院'
    elif x1 == '16':
        college = '社会科学学院'
    elif x1 == '17':
        college = '广告系'
    elif x1 == '18':
        college = '土木工程系'
    elif x1 == '20':
        college = '国际交流学院'
    elif x1 == '22':
        college = '数码艺术学院'
    elif x1 == '23':
        college = '中欧工程技术学院'
    elif x1 == '24':
        college = '管理学院'
    elif x1 == '25':
        college = '图书情报档案系'
    elif x1 == '27':
        college = '社区学院'
    elif x1 == '28':
        college = '社会学院'
    elif x1 == '29':
        college = '上海合作组织公共外交研究院'
    elif x1 == '30':
        college = 'MBA教育管理中心'
    elif x1 == '31':
        college = '音乐学院'
    elif x1 == '32':
        college = '公共艺术艺术实验教学中心'
    elif x1 == '80':
        college = '数学物理力学综合班(原)'
    elif x1 == '81':
        college = '钱伟长学院'
    elif x1 == '83':
        college = '生命科学基础班（原）'
    elif x1 == '84':
        college = '文史基础班（原）'
    elif x1 == '85':
        college = '体育学院'
    elif x1 == '86':
        college = '计算中心'
    elif x1 == '87':
        college = '实践教学'
    elif x1 == '88':
        college = '金工实习'
    elif x1 == '89':
        college = '电子实习'
    elif x1 == '90':
        college = '公益劳动'
    elif x1 == '91':
        college = '军事技能'
    elif x1 == '92':
        college = '图书馆'
    elif x1 == '93':
        college = '音乐学院'
    elif x1 == '94':
        college = '心理辅导中心'
    elif x1 == '95':
        college = '招生与毕业生就业工作办公室'
    elif x1 == '96':
        college = '纳米科学与技术研究中心'
    else:
        college = ''
    if x3 == '0':
        tag = '预科'
    elif x3 == '1':
        tag = '专科基础课'
    elif x3 == '1':
        tag = '专科基础课'
    elif x3 == '2':
        tag = '专科专业课'
    elif x3 == '3':
        tag = '专科、本科共同课程'
    elif x3 == '4':
        tag = '本科公共基础课'
    elif x3 == '5':
        tag = '本科学科基础课'
    elif x3 == '6':
        tag = '本科专业课'
    elif x3 == '7':
        tag = '硕士课程'
    elif x3 == '8':
        tag = '博士课程'
    elif x3 == '9':
        tag = '其他'
    elif x3 == 'A':
        tag = '实践环节课程'
    elif x3 == 'D':
        tag = '读书（或经典导读）与研讨'
    elif x3 == 'J':
        if x4 == 'H':
            tag = '经济管理大核心通识课'
        else:
            tag = '经济管理大类通识课'
    elif x3 == 'L':
        if x4 == 'H':
            tag = '理学工学类核心通识课'
        else:
            tag = '理学工学大类通识课'
    elif x3 == 'R':
        if x4 == 'H':
            tag = '人文社科类核心通识课'
        else:
            tag = '人文社科大类通识课'
    elif x3 == 'T':
        tag = '通识专题课'
    elif x3 == 'X':
        tag = '公共选修课'
    elif x3 == 'Y':
        tag = '新生研讨课'
    elif x3 == 'E' or x3 == 'S':
        if x4 == 'Y':
            tag = '高年级研讨课'
    else:
        tag = ''
    return college, tag
