import datetime
import re
import time

import requests
from bs4 import BeautifulSoup
from flask import current_app

from UHE.extensions import captcha_solver
from .models import Course, CourseOfTerm, Teacher, CourseSelectedRecord

TEACHER_CONVERTER = {
    '姓名:': 'name',
    '性别:': 'sex',
    '学历:': 'education',
    '学位:': 'degree',
    '职称:': 'title',
    '部门:': 'dept',
    '工号:': 'no',
    '自我简介': 'intro'
}


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

COLLEGE_CONVERTER = {
    '00': '特殊',
    '01': '理学院',
    '03': '外国语学院',
    '06': '法学院',
    '07': '通信与信息工程学院',
    '08': '计算机工程与科学学院',
    '09': '机电工程与自动化学院',
    '10': '材料科学与工程学院',
    '11': '环境与化学工程学院',
    '12': '生命科学学院',
    '13': '美术学院',
    '14': '上海电影学院',
    '15': '悉尼工商学院',
    '16': '社会科学学院',
    '17': '广告系',
    '18': '土木工程系',
    '20': '国际交流学院',
    '22': '数码艺术学院',
    '23': '中欧工程技术学院',
    '24': '管理学院',
    '25': '图书情报档案系',
    '27': '社区学院',
    '28': '社会学院',
    '29': '上海合作组织公共外交研究院',
    '30': 'MBA教育管理中心',
    '31': '音乐学院',
    '32': '公共艺术艺术实验教学中心',
    '80': '数学物理力学综合班(原)',
    '81': '钱伟长学院',
    '83': '生命科学基础班（原）',
    '84': '文史基础班（原）',
    '85': '体育学院',
    '86': '计算中心',
    '87': '实践教学',
    '88': '金工实习',
    '89': '电子实习',
    '90': '公益劳动',
    '91': '军事技能',
    '92': '图书馆',
    '93': '音乐学院',
    '94': '心理辅导中心',
    '95': '招生与毕业生就业工作办公室',
    '96': '纳米科学与技术研究中心'
}

COURSE_TYPE_CONVERTER = {
    '0': '预科',
    '1': '专科基础课',
    '1': '专科基础课',
    '2': '专科专业课',
    '3': '专科、本科共同课程',
    '4': '本科公共基础课',
    '5': '本科学科基础课',
    '6': '本科专业课',
    '7': '硕士课程',
    '8': '博士课程',
    '9': '其他',
    'A': '实践环节课程',
    'D': '读书（或经典导读）与研讨',
    'T': '通识专题课',
    'X': '公共选修课',
    'Y': '新生研讨课'
}


def get_xk(url):
    term = get_term(url)
    courselist = get_latest_course(url)
    save_courses(courselist, term)


def get_teacher(url, no):
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
        if text in TEACHER_CONVERTER.keys():
            td = next(tds)
            key = TEACHER_CONVERTER[text]
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
    now = datetime.datetime.now()
    for course in courselist:
        course_basic = {
            key: course.get(key) for key in ('no', 'name', 'teacher', 'credit', 'school', 'tags')
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
        course_basic['teacher_name'] = teacher.name
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
            course_of_term_db = CourseOfTerm(**course_detail).save()
        else:
            course_of_term_db = CourseOfTerm.objects(
                course=course_db, teacher_no=course['teacher_no']).first()
        course_record = CourseSelectedRecord.objects(
            course=course_of_term_db).first()
        if course_record is None:
            course_record = CourseSelectedRecord(
                course=course_of_term_db).save()
        course_record.enroll.append(course_of_term_db.enroll)
        course_record.capacity.append(course_of_term_db.capacity)
        course_record.updated.append(now)
        course_record.save()


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
            print('登录成功')
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
    names = ()
    for row in table.findAll("tr"):
        cells = row.findAll("td")
        course = {}
        names = ('teacher_no', 'teacher_name', 'time', 'place',
                 'capacity', 'enroll', 'campus', 'restrict', 'q_time', 'q_place')
        if len(cells) == 13:
            courseno = cells[0].get_text(strip=True)
            coursename = cells[1].get_text(strip=True)
            credit = cells[2].get_text(strip=True)
            teachid = cells[4].get('onclick')
            if teachid is not None:
                teachid = teachid[-10:-2]
            for i in range(3,13):
                key = names[i-3]
                course[key] = cells[i].get_text(strip=True)
        elif len(cells) == 10:
            teachid = cells[1].get('onclick')
            if teachid is not None:
                teachid = teachid[-10:-2]
            for i in range(0, 10):
                key = names[i]
                course[key] = cells[i].get_text(strip=True)
        if len(cells) == 13 or len(cells) == 10:
            school, tag = get_college_and_tag(courseno)
            course['no'] = courseno
            course['name'] = coursename
            course['credit'] = credit
            course['teacher_id'] = teachid,
            course['tags'] = [tag]
            course['school'] = school
            courselist.append(course)
    return courselist


def get_college_and_tag(courseid):
    x1 = courseid[0:2]
    x2 = courseid[2:4]
    x3 = courseid[4]
    x4 = courseid[5]
    if x1 in COLLEGE_CONVERTER.keys():
        college = COLLEGE_CONVERTER[x1]
    elif x1 == '02':
        if (x2 == '09') | (x2 == '75'):
            college = '社会学院'
        else:
            college = '文学院'
    elif x1 == '04':
        if x2 == '10':
            college = '图书情报档案系'
        elif x2 == '13' or x2 == '14'or x2 == '15':
            college = '经济学院'
        else:
            college = '管理学院'
    else:
        college = ''
    if x3 in COURSE_TYPE_CONVERTER.keys():
        tag = COURSE_TYPE_CONVERTER[x3]
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
    elif x3 == 'E' or x3 == 'S':
        if x4 == 'Y':
            tag = '高年级研讨课'
    else:
        tag = ''
    return college, tag
