from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask_login import current_user, login_required
import re
from UHE.feed.models import Feed
from UHE.message.models import Conversation
import requests
from bson import ObjectId
feeds = Blueprint('feeds', __name__)


@feeds.route('/<feed_id>/like')
def like(feed_id):
    if Feed.objects(id=feed_id,like__nin=[current_user.to_dbref()]).first() is not None:
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


class FeedsAPI(MethodView):
    decorators = [login_required]

    def get(self, feed_id=None):
        if not feed_id:
            page = int(request.args.get('page', 1))
            paginated_feeds = Feed.objects.paginate(
                page=page, per_page=5)
            return jsonify([feed.to_dict() for feed in paginated_feeds.items])
        else:
            feed = Feed.objects.get_or_404(id=feed_id)
            return jsonify(feed.to_dict())

    def post(self):
        args = request.get_json()
        feed_data = {
            'user': current_user.id,
            'feed_type': args.get('type', ''),
            'text': args.get('text', ''),
            'link_URL': args.get('linkURL', ''),
            'link_title': args.get('linkTitle', ''),
            'link_img': args.get('linkImg', ''),
            'img': args.get('img', [])
        }
        feed = Feed(**feed_data)
        feed.save()
        return jsonify({'id': str(feed.id)})

    def put(self, feed_id):
        feed = Feed.objects.get_or_404(id=feed_id)
        args = request.get_json()
        comments = Comment(user=current_user.id,
                           content=args['content'], message=pargrams['message'])
        message.save()
        conversation.messages.append(message)
        conversation.save()

    def delete(self, conversation_id):
        pass


feeds_view = FeedsAPI.as_view('feeds_api')
feeds.add_url_rule(
    '/', defaults={'feed_id': None}, view_func=feeds_view, methods=['GET', ])
feeds.add_url_rule(
    '/', view_func=feeds_view, methods=['POST', ])
feeds.add_url_rule('/<feed_id>', view_func=feeds_view,
                   methods=['GET', 'PUT', 'DELETE'])
