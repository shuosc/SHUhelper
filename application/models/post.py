from datetime import datetime
from flask_login import current_user
from application.extensions import db
from .user import User
from sqlalchemy.dialects import postgresql
from application.utils import CRUDMixin, TimeMixin
import uuid


class Post(db.Model, CRUDMixin, TimeMixin):
    id = db.Column(db.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    author_id = db.Column(db.String, db.ForeignKey('user.id'))
    type = db.Column(db.String)  # lost or found
    tags = db.Column(db.ARRAY(db.String, dimensions=1))
    title = db.Column(db.String)
    category = db.Column(db.String)
    content = db.Column(db.String)
    img_URLs = db.Column(postgresql.ARRAY(db.String, dimensions=1))
    site = db.Column(db.String)
    hit = db.Column(db.Integer, default=0)
    author = db.relationship('User', backref=db.backref(
        'posts', lazy=True))
