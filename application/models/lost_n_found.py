import datetime
from flask_login import current_user
from application.extensions import db
from application.models.user import User


class LostNFoundPost(db.Model):
    id = db.Column(db.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    author = db.Column(db.String, db.ForeignKey('user.id'))
    type = db.Column(db.String)
    title = db.Column(db.String)
    body = db.Column(db.String)
    primary_image_URL = db.Column(db.String)
    place = db.Column(db.String)
    action_time = db.Column(db.DateTime)
    created = db.Column(db.DateTime)
    status = db.Column(db.String)
    contact = db.Column(db.String)

