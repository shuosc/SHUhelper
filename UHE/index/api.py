from flask import Blueprint, jsonify, request, abort
from flask.views import MethodView
from flask_login import current_user

from UHE.link.models import Link

links = Blueprint('links', __name__)


@links.route('/<identifier>')
def get_link(identifier):
    link = Link.objects.get_or_404(identifier=identifier)
    return jsonify(link)
