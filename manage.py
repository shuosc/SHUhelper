from application.app import create_app
from application.extensions import db
from flask_migrate import Migrate, MigrateCommand
from application.services import calendar_installer
import click
# from application.models.user import User, UndergraduateStudent, GraduateStudent
# import application.plugins.SHU_course.manage as manage
# from application.extensions import celery
print('before app start')
app = create_app()

# manager = Manager(app)
migrate = Migrate(app, db)


@app.cli.command()
def dbmanger():
    MigrateCommand()


@app.cli.command()
def install_calendar():
    calendar_installer.install()
# import csv
# import json
# from application.models.user import Teacher

# _id
# degree
# sex
# title
# education
# name
# dept
# intro


# @app.cli.command()
# def update_users():
#     users = User.query.filter(User.user_type=None).all()
#     for user in users:
#         if user.id[2:4] == '12':
#             user.user_type = 'undergraduate_student'
#             result = db.engine.execute(
#                 "INSERT INTO undergraduate_student VALUES('{0}');".format(user.id))
#             # student =
#         elif user.id[2:4] == '72':
#             user.user_type = 'graduate_student'
#             result = db.engine.execute(
#                 "INSERT INTO graduate_student VALUES('{0}');".format(user.id))
#         user.save()


# @app.cli.command()
# def read_teachers():
#     with open('data/teachers2.json', 'r') as myFile:
#         # lines = csv.reader(myFile, delimiter=';')
#         data = json.load(myFile)
#         for line in data:
#             print(line)
#             teacher = Teacher.query.get(line['_id'])
#             if teacher is None:
#                 teacher = Teacher(
#                     id=line.get('_id'),
#                     degree=line.get('degree'),
#                     sex=line.get('sex'),
#                     title=line.get('title'),
#                     education=line.get('education'),
#                     username=line.get('name'),
#                     name=line.get('name'),
#                     dept=line.get('dept'),
#                     intro=line.get('intro')
#                 )
#                 teacher.save()


# from application.models.teaching_manage import Course, Class


# @app.cli.command()
# def read_courses():
#     with open('data/courses.json', 'r') as myFile:
#         # lines = csv.reader(myFile, delimiter=';')
#         data = json.load(myFile)
#         for line in data:
#             print(line)
#             course = Course.query.get(line['no'])
#             if course is None:
#                 course = Course(
#                     id=line.get('no'),
#                     name=line.get('name'),
#                     dept=line.get('school'),
#                     credit=line.get('credit')
#                 )
#                 course.save()


# @app.cli.command()
# def read_classes():
#     with open('data/classes2.json', 'r') as myFile:
#         # lines = csv.reader(myFile, delimiter=';')
#         data = json.load(myFile)
#         for line in data:
#             print(line)
#             old_class = Class.query.filter_by(class_id=line.get(
#                 'teacher_no'), course_id=line.get('course_no'), term=line.get('term')).all()
#             for _class in old_class:
#                 _class.delete()
#             teacher_id = line.get('teacher')
#             teacher = Teacher.query.get(teacher_id)
#             _class = Class(
#                 course_id=line.get('course_no'),
#                 term=line.get('term'),
#                 class_id=line.get('teacher_no'),
#                 campus=line.get('campus'),
#                 time=line.get('time'),
#                 classroom=line.get('place'),
#                 capacity=line.get('capacity'),
#                 enroll=line.get('enroll'),
#                 q_time=line.get('q_time'),
#                 q_place=line.get('q_place'),
#                 credit=line.get('credit'),
#                 status=line.get('status')
#             )
#             if teacher is None:
#                 _class.teacher_raw = line.get('teacher_name')
#             else:
#                 _class.teacher_id = teacher_id
#             _class.save()
# @app.cli.command()
# def get_xk_8080():
#     manage.get_xk('http://xk.shu.edu.cn:8080/')

# if __name__ == '__main__':
#     manager.run()
#     app.run(host='0.0.0.0',debug=True)
