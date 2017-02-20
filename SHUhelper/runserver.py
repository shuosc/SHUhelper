"""
This script runs the SHUhelper application using a development server.
"""

from os import environ
from SHUhelper import app
if __name__ == '__main__':
    app.debug = True
    app.run('localhost', 5555)
