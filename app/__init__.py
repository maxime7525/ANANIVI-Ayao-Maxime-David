from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_url           





app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager =  LoginManager()
login_manager.init_app(app)
login_manager.login_view ='connexion'

app.config['SECRET_KEY'] = "dnqzRUHq1AJ_oPzrKcrNVg"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config["UPLOADED_PHOTOS_DEST"] = "uploads"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
Bootstrap(app)
#{%extends "bootstrap/base.html"%}
#'mysql://username:motdepasse@localhost/blog.db'  

from app import routes
