from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField, DateTimeField, DateField, \
    SelectField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError, Optional, InputRequired, Email, EqualTo
from datetime import datetime

from app.models import User


class PostForm(FlaskForm):
    title = StringField('Post title', validators=[DataRequired()])
    content = TextAreaField('Write post here', validators=[DataRequired()])
    submit = SubmitField('Post')


class ForumForm(FlaskForm):
    book_title = StringField('Book Title', validators=[DataRequired()])
    author = StringField('author', validators=[DataRequired()])
    submit = SubmitField('Create Forum')


class LoginForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('submit')


class CreatePostForm(FlaskForm):
    title = StringField('Give your post a title', validators=[DataRequired()])
    content = StringField('What would you like to say', validators=[DataRequired()])
    submit = SubmitField('submit')

class ReplyForm(FlaskForm):
    content = StringField('What would you like to say', validators=[DataRequired()])
    submit = SubmitField('submit')

class RegistrationForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, name):
        user = User.query.filter_by(name=name.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')






