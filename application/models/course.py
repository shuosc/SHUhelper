from datetime import datetime
from flask_login import current_user
from application.extensions import db
from application.models.user import User
from application.extensions import ma
from marshmallow import post_load
from application.utils import CRUDMixin, TimeMixin


class Course(db.Model, CRUDMixin, TimeMixin):
    # id = db.Column(db.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    credit = db.Column(db.String)
    detail = db.Column(db.String)
    dept = db.Column(db.String)

    @classmethod
    def from_json(cls, json_post):
        return cls(
            id=json_post.get('id'),
            name=json_post.get('name'),
            credit=json_post.get('credit'),
            detail=json_post.get('detail')
        )

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'credit': self.credit
        }


class CourseScheme(ma.ModelSchema):
    class Meta:
        model = Course

    @post_load
    def load(self, data):
        return Course(**data)


course_schema = CourseScheme()
courses_schema = CourseScheme(many=True)
