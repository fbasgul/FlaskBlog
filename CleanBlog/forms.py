from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Length,Email
from wtforms.widgets.core import TextArea

class RegisterForm(FlaskForm):
    name=StringField('Name',validators=[DataRequired(),Length(min=2,max=20)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=2,max=20)])
    submit=SubmitField('Sign')

class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=2,max=20)])
    submit=SubmitField('Login')

class PostForm(FlaskForm):
    title=StringField('Title',validators=[DataRequired()])
    subtitle=StringField('SubTitle',validators=[DataRequired()])
    post_text=TextAreaField('Post Text',validators=[DataRequired()])
    submit=SubmitField('Add Post')
    submitedit=SubmitField('Change Post')
