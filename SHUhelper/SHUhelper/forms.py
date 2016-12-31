from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, email
class LoginForm(FlaskForm):
    #username = StringField('Username', validators=[DateaRequired()])
    email = StringField('Email',validators=[DataRequired(), Length(1,64), email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')


class CommentForm(FlaskForm):
    username = StringField('昵称',validators=[DataRequired()])
    comment = TextAreaField('评论',validators=[DataRequired()])
    submit = SubmitField(u'submit')