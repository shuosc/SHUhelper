from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from SHUhelper.config import basedir
import os
from datetime import datetime
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    postid = db.Column(db.String(50))
    username = db.Column(db.String(20))
    comment = db.Column(db.String(240))
    time = db.Column(db.DateTime, default=datetime.utcnow())
    #def __init__(self, id, postid, username, comment):
    #    self.id = id
    #    self.postid = postid
    #    self.username = username
    #    self.comment = comment

    def __repr__(self):
        return '<User %r>' % self.username