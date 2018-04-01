from UHE.app import create_app
from UHE.extensions import db
from flask_script import Manager,Shell
from flask_migrate import Migrate,MigrateCommand
import click
# import UHE.plugins.SHU_course.manage as manage
# from UHE.extensions import celery 
print('before app start')
app = create_app()
manager = Manager(app)
migrate = Migrate(app,db)

def make_shell_context():
    return dict(app=app,db=db)
manager.add_command('db',MigrateCommand)
manager.add_command('shell',Shell(make_context=make_shell_context))
print('app start')
# @app.cli.command()
# def get_xk_8080():
#     manage.get_xk('http://xk.shu.edu.cn:8080/')

if __name__ == '__main__':
    manager.run()
#     app.run(host='0.0.0.0',debug=True)