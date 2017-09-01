import datetime

from UHE.calendar.models import Activity
from UHE.client import Services

def make_token():
    """
    generate random token, length is 8.
    """
    import random
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    sa = []
    for i in range(8):
        sa.append(random.choice(seed))
    salt = ''.join(sa)
    return salt


def this_year(date=datetime.datetime.now()):
    year_event = Activity.objects(
        start__gte=date, end__lte=date, key='year').first()
    if year_event is not None:
        return int(year_event.args.split('_')[-1])
    else:
        return 0


def this_week(date=datetime.datetime.now()):
    week_event = Activity.objects(
        start__gte=date, end__lte=date, key='week').first()
    if week_event is not None:
        return int(week_event.args.split('_')[-1])
    else:
        return 0


def this_term(date=datetime.datetime.now()):
    term_event = Activity.objects(
        start__gte=date, end__lte=date, key='term').first()
    if term_event is not None:
        return int(term_event.args.split('_')[-1])
    else:
        return 0


def this_course(date=datetime.datetime.now()):
    course_event = Activity.objects(
        start__gte=date, end__lte=date, key='course_basic').first()
    if course_event is not None:
        return int(course_event.args.split('_')[-1])
    else:
        return 0


def validate(card_id, password):
    client = Services(card_id=card_id,password=password)
    if client.login() and client.get_data():
        result = {
            'success': True,
            'name': client.data['name'],
            'card_id': card_id
        }
    else:
        result = {
            'success': False
        }
    return result