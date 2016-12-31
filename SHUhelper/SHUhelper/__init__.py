"""
The flask application package.
"""

from flask import Flask
from flask_migrate import Migrate, MigrateCommand
app = Flask(__name__)
import SHUhelper.views