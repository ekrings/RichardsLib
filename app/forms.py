from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField, DateTimeField, DateField, \
    SelectField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError, Optional, InputRequired
from datetime import datetime
from app.models import User

class PostForm(FlaskForm):
    title = StringField('Post title', validators=[DataRequired()])
    content = TextAreaField('Write post here', validators=[DataRequired()])
    submit = SubmitField('Post')
class ForumForm(FlaskForm):
    book_title = StringField('Book Title', validators=[DataRequired()])
    author = PasswordField('author', validators=[DataRequired()])
    submit = SubmitField('Create Forum')
class LoginForm(FlaskForm):
    name = StringField('Bard Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('submit')
class CreatePostForm(FlaskForm):
    title = StringField('Give your post a title', validators=[DataRequired()])
    content = StringField('What would you like to say', validators=[DataRequired()])
    submit = SubmitField('submit')
