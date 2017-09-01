import re
from bs4 import BeautifulSoup


def detect_conflict(data):
    time_list_raw = [[], [], [], [], []]
    for days in time_list_raw:
        for i in range(0, 13):
            days.append(0)
    for time_list in data:
        for j in range(0, 5):
            for i in range(0, 13):
                if time_list[j][i] == 0:
                    time_list_raw[j][i] = time_list_raw[j][i] + 1
    return time_list_raw


def list_init():
    time_table = [[], [], [], [], []]
    for days in time_table:
        for i in range(0, 13):
            days.append(1)
    return time_table


def get_json_from_course_table(content):
    import json
    table = re.search(
        r'<table class="tbllist">([\s\S]*?)</table>', content, flags=0).group(0)
    soup = BeautifulSoup(table, "html.parser")
    table = soup.find("table")
    course_list = []
    for row in table.findAll("tr")[2:]:
        cells = row.findAll("td")[1:]
        data = {
            'courseno': cells[0].get_text(strip=True),
            'coursename': cells[1].get_text(strip=True),
            'teachno': cells[2].get_text(strip=True),
            'teachname': cells[3].get_text(strip=True),
            'credit': cells[4].get_text(strip=True),
            'coursetime': cells[5].get_text(strip=True),
            'courseplace': cells[6].get_text(strip=True),
            'campus': cells[7].get_text(strip=True),
            'qtime': cells[8].get_text(strip=True),
            'qplace': cells[9].get_text(strip=True)
        }
        course_list.append(data)
    return json.dumps(course_list)


def get_binary_json_from_course_table(content, week):
    import json
    cn_num = {
        u'一': 1,
        u'二': 2,
        u'三': 3,
        u'四': 4,
        u'五': 5,
    }
    time_table = list_init()
    table = re.search(
        r'<table class="tbllist">([\s\S]*?)</table>', content, flags=0).group(0)
    soup = BeautifulSoup(table, "html.parser")
    table = soup.find("table")
    for row in table.findAll("tr")[3:]:
        cells = row.findAll("td")[1:]
        if len(cells) == 0:
            break
        coursename = cells[1].get_text(strip=True)
        coursetime = cells[5].get_text(strip=True)
        while True:
            # noinspection Annotator,Annotator,Annotator,Annotator
            time = re.search(
                r'([\u4e00|\u4e8c|\u4e09|\u56db|\u4e94])([0-9]+)-([0-9]+)\s*(?:([\u5355|\u53cc|])|\((?:([0-9]+)-([0-9]+)\u5468)\)|\((?:([0-9]+),([0-9]+)\u5468)\))*', coursetime)
            # noinspection Annotator,Annotator,Annotator,Annotator
            coursetime = re.sub(
                r'([\u4e00|\u4e8c|\u4e09|\u56db|\u4e94])([0-9]+)-([0-9]+)\s*(?:([\u5355|\u53cc|])|\((?:([0-9]+)-([0-9]+)\u5468)\)|\((?:([0-9]+),([0-9]+)\u5468)\))*', '', coursetime, 1)
            if time is None:
                break
            day = cn_num[time.group(1)]
            start = int(time.group(2))
            end = int(time.group(3))
            in_this_week = False
            if time.group(4) is not None:
                if time.group(4) == u'单':
                    if week % 2 == 1:
                        in_this_week = True
                else:
                    if week % 2 == 0:
                        in_this_week = True
            elif time.group(5) is not None:
                if int(time.group(5)) <= week <= int(time.group(6)):
                    in_this_week = True
            elif time.group(7) is not None:
                if week == int(time.group(7)) or week == int(time.group(8)):
                    in_this_week = True
            else:
                in_this_week = True
            if in_this_week:
                for i in range(start, end + 1):
                    time_table[day - 1][i - 1] = 0
    return time_table
