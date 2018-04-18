from datetime import datetime
from functools import reduce

import requests
from flask import Blueprint, Flask, jsonify, request,current_app
from flask.views import MethodView
from flask_login import current_user, login_required

from application.extensions import db
from application.models.lost_n_found import LostNFoundPost as Post

lost_n_found = Blueprint('lost_n_found', __name__)

class LostNFoundAPI(MethodView):
    decorators = [login_required]

    def get(self, post_id):
        if post_id is None:
            posts_type = request.args.get('type', 'found')
            author_id = request.args.get('authorID')
            page = request.args.get('page')
            if author_id is None:
                posts = Post.query.filter_by(type=posts_type).order_by(Post.created.desc()).all()
                return jsonify(posts=[post.to_json() for post in posts])
        else:
            post = Post.query.filter_by(id=post_id).first()
            return jsonify(post=post.to_json())

    def post(self):
        now = datetime.now()
        nowaday = datetime(now.year, now.month, now.day)
        json = request.json
        json['userID'] = current_user.id
        post = Post.from_json(json)

        if check_restrict(post, current_user.id) == False:
            return jsonify(msg='您当日借教室时长配额不足'), 400
        if check_room_available(post) == False:
            return jsonify(msg='该时间段已被占用'), 400
        timedelta = post.date - nowaday
        if timedelta.days < 0 or timedelta.days > 3:
            return jsonify(msg='该日无法预约'), 400
        if timedelta.days == 0 and current_app.school_time.get_course() > post.start:
            return jsonify(msg='您选择的时段已过，无法预约'), 400
        post.save()
        return jsonify(post=post.to_json())

    def delete(self, post_id):
        if post_id is None:
            return jsonify(msg="无权限"), 401
        else:
            post = Post.query.filter_by(id=post_id).first()
            if not post.user_id == current_user.id:
                return jsonify(msg="无权限"), 401
            post.delete()
            return jsonify(sucroom_posts=True)

    def put(self, post_id):
        post = Post.query.filter_by(id=post_id).first()
        if not post.user_id == current_user.id:
            return jsonify(msg="无权限"), 401
        json = request.json
        end = json['end']
        if end >= post.start and end <=post.end:
            post.end = end
            post.save()
        return jsonify(post=post.to_json())

view = LostNFoundAPI.as_view('lost_n_found_api')
lost_n_found.add_url_rule('/', defaults={'post_id': None},
                 view_func=view, methods=['GET', ])
lost_n_found.add_url_rule('/', view_func=view, methods=['POST', ])
lost_n_found.add_url_rule('/<post_id>', view_func=view,
                 methods=['GET', 'PUT', 'DELETE'])
