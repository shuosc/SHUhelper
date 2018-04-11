from application.app import create_app
from application.extensions import db
from flask_migrate import Migrate,MigrateCommand
import click
# import application.plugins.SHU_course.manage as manage
# from application.extensions import celery 
print('before app start')
app = create_app()

# manager = Manager(app)
migrate = Migrate(app,db)
@app.cli.command()
def dbmanger():
    MigrateCommand()


# @app.cli.command()
# def get_xk_8080():
#     manage.get_xk('http://xk.shu.edu.cn:8080/')

# if __name__ == '__main__':
#     manager.run()
#     app.run(host='0.0.0.0',debug=True)