from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask_login import current_user

from .models import Course, Evaluation

evaluations = Blueprint('evaluations', __name__)


@evaluations.route('/<oid>/like')
def like(oid):
    if current_user.is_anonymous:
        user = User.objects(card_id="00000001").first()
        Evaluation.objects(id=oid).update_one(push__like=user.to_dbref())
    elif Evaluation.objects(id=oid, like__nin=[current_user.to_dbref()]).first() is not None:
        Evaluation.objects(id=oid).update_one(
            push__like=current_user.to_dbref())
    else:
        Evaluation.objects(id=oid).update_one(
            pull__like=current_user.to_dbref())
    return jsonify(id=str(oid))


class EvaluationAPI(MethodView):
    def get(self, evaluation_id=None):
        if not evaluation_id:
            args = request.args
            if args.get('course'):
                evaluations = Evaluation.objects(course=args['course'])
                return jsonify(evaluations)
            else:
                page = int(args['page'])
                per_page = args.get('per_page', 10)
                evaluations = Evaluation.objects(
                )[per_page * (page - 1):per_page * (page)]
                return jsonify([evaluation.to_dict() for evaluation in evaluations])

    def post(self):
        args = request.get_json()
        course = Course.objects(id=args['course']).get_or_404()
        evaluation = Evaluation(
            user=current_user.id, display_name=args['name'],
            rating=args['rating'], text=args['text'], term=args['term'], course=args['course'])
        evaluation.save()
        evaluations = Evaluation.objects(course=args['course'])
        count = evaluations.count()
        star = 0
        for evaluation in evaluations:
            star += evaluation.rating
        course.rating = star / count
        course.evaluations_count = count
        course.save()
        return jsonify(success=True)


evaluation_view = EvaluationAPI.as_view('evaluation_api')
evaluations.add_url_rule(
    '/', view_func=evaluation_view, methods=['GET', 'POST'])
evaluations.add_url_rule('/<evaluation_id>', view_func=evaluation_view,
                         methods=['GET'])
