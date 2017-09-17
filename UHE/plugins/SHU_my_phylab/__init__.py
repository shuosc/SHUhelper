import datetime

from flask import Blueprint, jsonify, request, current_app
from flask_login import current_user, login_required

from UHE.client import Phylab
from UHE.extensions import celery, captcha_solver
from UHE.plugins import UHEPlugin
from UHE.user.models import UserData

# from celery.contrib.methods import task_method
__plugin__ = "SHUMyPhylab"


my_phylab = Blueprint('my_phylab', __name__)


@my_phylab.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'GET':
        data = UserData.objects(user=current_user.id,
                                identifier=__plugin__).get_or_404()
        return jsonify(data)
    else:
        post_data = request.get_json()
        user_data = UserData.objects(
            user=current_user.id, identifier=__plugin__).first()
        if user_data is None:
            user_data = UserData(identifier=__plugin__,
                                 user=current_user.id, status='none')
            user_data.save()
        task = get_phylab.delay(current_user.id, post_data['password'])
        return jsonify(success=task.id)


@my_phylab.route('/status')
@login_required
def status():
    data = UserData.objects(user=current_user.id,
                            identifier=__plugin__).get_or_404()
    return jsonify(status=data.status)


@my_phylab.route('/sync', methods=['GET', 'POST'])
def sync_index():
    if request.method == 'GET':
        data = UserData.objects(user=current_user.id,
                                identifier=__plugin__).get_or_404()
        return jsonify(data)
    else:
        post_data = request.get_json()
        user_data = UserData.objects(
            user=current_user.id, identifier=__plugin__).first()
        if user_data is None:
            user_data = UserData(identifier=__plugin__,
                                 user=current_user.id, status='none')
            user_data.save()
        else:
            if user_data.status == 'pending':
                return jsonify(status='pending')
        task = get_phylab(current_user.id, post_data['password'])
        return jsonify(success='ok')


@celery.task
def get_phylab(card_id, password):
    user_data = UserData.objects(user=card_id, identifier=__plugin__).first()
    user_data.status = 'pending'
    user_data.save()
    try:
        client = Phylab(card_id, password)
        client.captcha = captcha_solver.create(
            client.captcha_img, site='phylab')['Result']
        print(card_id, password)
        client.login()
        client.get_data()
    except Exception as e:
        user_data.status = 'failed'
        user_data.save()
        print('error')
        raise e
    user_data.data = client.to_json()
    user_data.status = 'success'
    user_data.last_modified = datetime.datetime.now()
    user_data.lock_save(password)


class SHUMyPhylab(UHEPlugin):
    settings_key = 'SHU_my_phylab'

    def setup(self, app):
        # self.app = current_app
        # print(current_app)
        current_app.register_blueprint(my_phylab, url_prefix='/phylab')

        print('setup', __plugin__)
        # print(current_app.url_map)

    def install(self, app):
        pass

    def uninstall(self):
        print('uninstall')
        pass
