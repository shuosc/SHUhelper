from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField
from wtforms.validators import DataRequired
class CommentForm(FlaskForm):
    username = StringField('昵称',validators=[DataRequired()])
    comment = TextAreaField('评论',validators=[DataRequired()])
    submit = SubmitField(u'submit')