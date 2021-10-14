from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app=Flask(__name__)
app.config['SECRET_KEY']='falanfistuk'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///myblog.db'
db=SQLAlchemy(app)

login_manager=LoginManager(app)

from CleanBlog import routes