from flask import Blueprint, jsonify, request, abort
from flask.views import MethodView
from flask_login import current_user

from .models import Link

index = Blueprint('index', __name__)


@index.route('/link/<identifier>')
def get_link(identifier):
    link = Link.objects.get_or_404(identifier=identifier)
    return jsonify(link)
