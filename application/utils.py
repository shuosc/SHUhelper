from application.services.sim_clients import Services
import ast
import os
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

def validate(card_id, password):
    client = Services(card_id=card_id, password=password)
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
