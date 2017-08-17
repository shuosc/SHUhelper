#coding=utf-8
import re
import csv
import json

def list_init():
    semester_list = []
    for i in range(0,10):
        semester_list.append([([1] * 13) for i in range(0,5)])
    return semester_list

f = open("classroomdata.txt", "w")
ff = open("classrooms.txt", "w")
classroom_dict = {}
cn_num={
    '一':1,
    '二':2,
    '三':3,
    '四':4,
    '五':5,
}
csvfile = open('Course_Of_Term.csv', 'r', encoding='utf-8')
lines = csv.reader(csvfile)
for line in lines:
    if not line:
        continue
    if line[11] != '2017_1':
        continue
    raw_time=line[2]
    classroom=line[3]
    if re.search(r'^([A-G]|[A-G]J)[0-9][0-9][0-9]$',classroom,flags=0)==None:
        continue
    if classroom not in classroom_dict:
        classroom_dict[classroom] = list_init()
        ff.write(classroom+'\n')
    while(True):
        time = re.search(r'([\u4e00|\u4e8c|\u4e09|\u56db|\u4e94])([0-9]+)-([0-9]+)\s*(?:([\u5355|\u53cc|])|\((?:([0-9]+)-([0-9]+)\u5468)\)|\((?:([0-9]+),([0-9]+)\u5468)\))*',raw_time,flags=0)
        if time == None:
            break
        raw_time = re.sub(r'([\u4e00|\u4e8c|\u4e09|\u56db|\u4e94])([0-9]+)-([0-9]+)\s*(?:([\u5355|\u53cc|])|\((?:([0-9]+)-([0-9]+)\u5468)\)|\((?:([0-9]+),([0-9]+)\u5468)\))*','',raw_time,1)
        
        day = cn_num[time.group(1)]
        start = int(time.group(2))
        end = int(time.group(3))
        for week in range(1,11):
            in_this_week = False
            if time.group(4)!=None:
                if time.group(4) == '单':
                    if week%2==1:
                        in_this_week=True
                else:
                    if week%2==0:
                        in_this_week=True
            elif time.group(5)!=None:
                if week>=int(time.group(5)) and week<=int(time.group(6)):
                    in_this_week=True
            elif time.group(7)!=None:
                if week==int(time.group(7)) or week==int(time.group(8)):
                    in_this_week=True
            else:
                in_this_week=True
            if in_this_week:
                for i in range(start,end+1):
                    classroom_dict[classroom][week-1][day-1][i-1] = 0


f.write(json.dumps(classroom_dict))
f.close()
ff.close()


        

