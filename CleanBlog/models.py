from CleanBlog import db,login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30),nullable=False)
    email=db.Column(db.String(50),unique=True,nullable=False)
    password=db.Column(db.String(30),nullable=False)
    posts=db.relationship('Post',backref='user',lazy=True)

    def __init__(self,name,email,password):
        self.email=email
        self.name=name
        self.password=password

    def __repr__(self):
        return f'User: {self.name}, Email: {self.email}'

class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String,nullable=False)
    subtitle=db.Column(db.String,nullable=False)
    post_date=db.Column(db.DateTime,nullable=False,default=datetime.now)
    post_text=db.Column(db.Text,nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __init__(self,title,subtitle,post_text,user):
        self.title=title
        self.subtitle=subtitle
        self.post_text=post_text
        self.user=user

    def __repr__(self):
        return f'Post: {self.title}, {self.subtitle}'
