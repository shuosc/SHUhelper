from UHE.plugins.SHU_api.client import Services
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
