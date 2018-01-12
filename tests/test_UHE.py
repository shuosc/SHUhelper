from UHE.app import create_app
from UHE.user.api import login
from UHE.calendar.api import now
import flask_login
app = create_app()

def test_app_start():
    return True
