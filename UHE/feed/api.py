import re

import requests
from flask import Blueprint, jsonify, request, abort
from flask.views import MethodView
from flask_login import current_user, login_required
from UHE.user.models import User
from UHE.feed.models import Feed

feeds = Blueprint('feeds', __name__)


@feeds.route('/<feed_id>/like')
def like(feed_id):
    if current_user.is_anonymous:
        user = User.objects(card_id="00000001").first()
        Feed.objects(id=feed_id).update_one(push__like=user.to_dbref())
    elif Feed.objects(id=feed_id, like__nin=[current_user.to_dbref()]).first() is not None:
        Feed.objects(id=feed_id).update_one(push__like=current_user.to_dbref())
    else:
        Feed.objects(id=feed_id).update_one(pull__like=current_user.to_dbref())
    return jsonify(id=str(feed_id))


@feeds.route('/link')
def get_link_detail():
    link = request.args.get('link')
    s = requests.Session()
    r = s.get(link, timeout=10)
    # print(r.text)
    title = re.search(r'<title>([\s\S]*?)</title>', r.text, flags=0).group(1)
    # print(title(encoding='utf-8'))
    return jsonify(title=title)



class CommonFeedsAPI(MethodView):
    def get(self, feed_id=None):
        if not feed_id:
            namespace = request.args.get('namespace', 'ordinary')
            page = int(request.args.get('page', 1))
            paginated_feeds = Feed.objects(namespace=namespace).paginate(
                page=page, per_page=10)
            total = Feed.objects(namespace=namespace).count()
            return jsonify(total=total, feeds=[feed.to_dict() for feed in paginated_feeds.items])
        else:
            feed = Feed.objects.get_or_404(id=feed_id)
            return jsonify(feed.to_dict())

    def post(self):
        args = request.get_json()
        feed_data = {
            'user': current_user.id,
            'namespace': args.get('namespace', 'ordinary'),
            'text': args.get('text', ''),
            'link_URL': args.get('linkURL', ''),
            'link_title': args.get('linkTitle', ''),
            'link_img': args.get('linkImg', ''),
            'img': args.get('img', [])
        }
        if feed_data['text'] is None:
            abort(401)
        feed = Feed(**feed_data)
        feed.save()
        return jsonify({'id': str(feed.id)})

    def put(self, feed_id):
        pass

    def delete(self, feed_id):
        feed = Feed.objects(id=feed_id).get_or_404()
        if feed.user.id == current_user.id:
            feed.delete()
        else:
            abort(401)
        return jsonify(status='ok')


class RealnameFeedsAPI(CommonFeedsAPI):
    decorators = [login_required]

class AnonymousFeedsAPI(CommonFeedsAPI):
   
    def post(self):
        args = request.get_json()
        feed_data = {
            'user': current_user.id,
            'display_name': args.get('name', '匿名'),
            'namespace': args.get('namespace', 'ordinary'),
            'text': args.get('text', ''),
            'link_URL': args.get('linkURL', ''),
            'link_title': args.get('linkTitle', ''),
            'link_img': args.get('linkImg', ''),
            'img': args.get('img', [])
        }
        if len(feed_data['text']) == 0:
            abort(405)
        feed = Feed(**feed_data)
        feed.save()
        return jsonify({'id': str(feed.id)})

    def delete(self, feed_id):
        abort(401)


realname_feeds_view = RealnameFeedsAPI.as_view('feeds_api')
feeds.add_url_rule(
    '/', defaults={'feed_id': None}, view_func=realname_feeds_view, methods=['GET', ])
feeds.add_url_rule(
    '/', view_func=realname_feeds_view, methods=['POST', ])
feeds.add_url_rule('/<feed_id>', view_func=realname_feeds_view,
                   methods=['GET', 'PUT', 'DELETE'])

anonymous_feeds_view = AnonymousFeedsAPI.as_view('anonymous_feeds_api')
feeds.add_url_rule(
    '/anonymous/', view_func=anonymous_feeds_view, methods=['POST', ])
feeds.add_url_rule(
    '/anonymous/', defaults={'feed_id': None}, view_func=anonymous_feeds_view, methods=['GET', ])
feeds.add_url_rule(
    '/anonymous/', view_func=anonymous_feeds_view, methods=['POST', ])
feeds.add_url_rule('/<feed_id>', view_func=anonymous_feeds_view,
                   methods=['GET', 'PUT', 'DELETE'])
