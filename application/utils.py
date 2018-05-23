# from application.services.sim_clients import Services
import ast
import os
from application.extensions import db
from datetime import datetime


def register_api(blue_print, view, endpoint, url, pk='id', pk_type='int'):
    view_func = view.as_view(endpoint)
    blue_print.add_url_rule(url, defaults={pk: None},
                            view_func=view_func, methods=['GET', ])
    blue_print.add_url_rule(url, view_func=view_func, methods=['POST', ])
    blue_print.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func,
                            methods=['GET', 'PUT', 'DELETE'])


def current_day_seconds():
    now = datetime.now()
    return (now.hour*60+now.minute)*60+now.second


def seconds_to_ten_minutes(seconds):
    return (seconds / 60) / 10


def current_ten_minutes():
    seconds = current_day_seconds()
    return seconds_to_ten_minutes(seconds)


class TimeMixin(object):
    created_at = db.Column(db.DateTime,
                           default=datetime.now)
    updated_at = db.Column(db.DateTime,
                           default=datetime.now)


class CRUDMixin(object):
    is_deleted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "<{}>".format(self.__class__.__name__)

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()

    def save(self):
        """Saves the object to the database."""
        db.session.add(self)
        db.session.commit()
        return self

    # def update(self):
    #     self.updated_at = datetime.now()
    #     db.session.add(self)
    #     db.session.commit()
    #     return self

    def delete(self, soft=False):
        """Delete the object from the database."""
        if soft:
            self.is_deleted = True
            self.save()
        else:
            db.session.delete(self)
            db.session.commit()
        return self


def make_token():
    """
    generate random token, length is 8.
    """
    import random
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    sa = [random.choice(seed) for i in range(8)]
    salt = ''.join(sa)
    return salt


def app_config_from_env(app, prefix="application_"):
    """Retrieves the configuration variables from the environment.
    Set your environment variables like this::
        export application_SECRET_KEY="your-secret-key"
    and based on the prefix, it will set the actual config variable
    on the ``app.config`` object.
    :param app: The application object.
    :param prefix: The prefix of the environment variables.
    """
    for key, value in iter(os.environ.items()):
        if key.startswith(prefix):
            key = key[len(prefix):]
            try:
                value = ast.literal_eval(value)
            except (ValueError, SyntaxError):
                pass
            app.config[key] = value
    return app

# def validate(card_id, password):
#     client = Services(card_id=card_id, password=password)
#     if client.login() and client.get_data():
#         result = {
#             'success': True,
#             'name': client.data['name'],
#             'card_id': card_id
#         }
#     else:
#         result = {
#             'success': False
#         }
#     return result
