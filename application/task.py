# import flask.signals.Namespace
from blinker import signal

from application.extensions import celery


@celery.task
def signal_scheduler(signal_name,sender):
    signal(signal_name).send(sender)

def signal_register(app):
    app.signals = {}
    pass
