import datetime

from flask import Blueprint, jsonify, request, current_app
# from flask_login import current_user.
from flask.views import MethodView
from flask_login import current_user, login_required
from mongoengine.queryset.visitor import Q

from .models import Activity, Event

# from UHE.utils import this_course, this_term, this_week

events = Blueprint('events', __name__)


@events.route('/now')
def now():
    time = current_app.school_time.time
    return jsonify(year=time.year, term=time.term, 
        week=time.week, course=time.course,day=time.day)

class EventAPI(MethodView):
    decorators = [login_required]

    def get(self, event_id=None, page=1):
        if not event_id:
            now = datetime.datetime.now()
            start_text = request.args.get(
                'start', now.timestamp())
            end_text = request.args.get(
                'end', now.timestamp())
            start = datetime.datetime.utcfromtimestamp(int(start_text))
            end = datetime.datetime.utcfromtimestamp(int(end_text))
            activities = Activity.objects(
                Q(visible='public') & (
                (Q(start__lte=end) & Q(end__gte=end)) | (Q(start__gte=start) & Q(end__lte=end)))).paginate(page=page,
                                                                                                           per_page=100)
            return jsonify([activity.to_dict() for activity in activities.items])
        else:
            event = Event.objects.get_or_404(id=event_id)
            return jsonify(event)

    def post(self):
        now = datetime.datetime.now()
        args = request.get_json()
        event = Event(
            user=current_user.id,
            title=args.get('title', ''),
            remark=args.get('remark', ''),
        )
        event.save()
        start_text = args.get(
            'start', '{}-{}-{}-{}-{}'.format(now.year, now.month, now.day, 0, 0))
        end_text = args.get(
            'end', '{}-{}-{}-{}-{}'.format(now.year, now.month, now.day + 1, 0, 0))
        start = datetime.datetime(*(start_text.split('-')))
        end = datetime.datetime(*(end_text.split('-')))
        sub_event = Activity(
            category=args.get('category', ''),
            event=event,
            title=args.get('title', ''),
            place=args.get('place', ''),
            start=start,
            end=end
        )
        sub_event.save()
        return jsonify(activity=sub_event)

    # noinspection SpellCheckingInspection
    def put(self, conversation_id):
        pass
        # conversation = Conversation.objects.get_or_404(id=conversation_id)
        # args = request.get_json()
        # print(args)
        # message = Message(sender=current_user.id,
        #                   message_type="private", content=args['content'])
        # message.save()
        # Conversation.objects(id=conversation_id).update_one(
        #     push__messages=message)
        # return jsonify(message=str(message.id))

    def delete(self, conversation_id):
        pass


events_view = EventAPI.as_view('event_api')
events.add_url_rule(
    '/', defaults={'event_id': None}, view_func=events_view, methods=['GET', ])
events.add_url_rule(
    '/', view_func=events_view, methods=['POST', ])
events.add_url_rule('/<event_id>', view_func=events_view,
                    methods=['GET', 'PUT', 'DELETE'])
