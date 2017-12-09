import datetime

from flask import Blueprint, abort, current_app, jsonify, request
from mongoengine.queryset.visitor import Q
from flask.views import MethodView
from UHE.goods.models import Goods
import json
goods = Blueprint('goods', __name__)


class GoodsAPI(MethodView):
    def get(self):
        goods = Goods.objects()
        return jsonify([good.to_dict() for good in goods])

    def put(self, goods_id):
        Goods.objects(id=goods_id).update_one(
            push__record=datetime.datetime.now())
        goods = Goods.objects()
        return jsonify([good.to_dict() for good in goods])

    def delete(self, goods_id):
        Goods.objects(id=goods_id).update_one(pop__record=1)
        goods = Goods.objects()
        return jsonify([good.to_dict() for good in goods])


goods_view = GoodsAPI.as_view('goods_api')
goods.add_url_rule(
    '/', view_func=goods_view, methods=['GET', ])
goods.add_url_rule('/<goods_id>', view_func=goods_view,
                   methods=['PUT', 'DELETE'])
