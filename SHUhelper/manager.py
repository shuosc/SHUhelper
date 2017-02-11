"""
This script runs the SHUhelper application using a development server.
"""

from os import environ
from SHUhelper import app
from SHUhelper.config import manager
from flask_migrate import Migrate, MigrateCommand
from flask_script import Shell
from SHUhelper.models import *
migrate = Migrate(app, db)
def make_shell_context():
    return dict(app=app, db=db, User=User, Comment=Comment)
manager.add_command('db', MigrateCommand)
manager.add_command("shell", Shell(make_context=make_shell_context))
if __name__ == '__main__':
    manager.run()
