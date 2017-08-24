from UHE.app import create_app
from UHE.extensions import celery
from UHE.calendar import clock
from celery.schedules import crontab
from blinker import signal
app = create_app()
signal('app_start').send()
# celery.task()
# @celery.task
# def


# @celery.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds.
#             # times = [(8, 0), (8, 55), (10, 0), (10, 55), (12, 10), (13, 5),
#                 #  (14, 10), (15, 5), (16, 0), (16, 55), (18, 0), (18, 55), (19, 50)]
#     # sender.add_periodic_task(10.0, clock.s('sss'), name='add every 10')

#     # Calls test('world') every 30 seconds
#     # sender.add_periodic_task(30.0, clock.s('world'))
#     # sender.add_periodic_task(
#     #     crontab(minute='*'),
#     #     clock.s('Happy Mondays!'),
#     # )
#     # Executes every Monday morning at 7:30 a.m.
#     # sender.add_periodic_task(
#     #     crontab(minute='*'),
#     #     clock.s('Happy Mondays!'),
#     # )
#     pass

# @celery.task
# def test(arg):
#     print(arg)
