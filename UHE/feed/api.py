from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask_login import current_user, login_required
import re
from UHE.feed.models import Feed
from UHE.message.models import Conversation
import requests
feeds = Blueprint('feeds', __name__)


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

    def get(self, feed_id=None, page=1):
        if not feed_id:
            paginated_feeds = Feed.objects.paginate(
                page=page, per_page=20)
            return jsonify([feed.to_dict() for feed in paginated_feeds.items])
            # return jsonify(paginated_feeds)
        else:
            feed = Conversation.objects.get_or_404(id=feed_id)
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
