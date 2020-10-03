from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from os import environ
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY']='Guess_Hard'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL') or 'sqlite:///myDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
csrf=CSRFProtect(app)
db=SQLAlchemy(app)
login=LoginManager(app)
login.init_app(app)
import routes, models

#login.login_view = 'login'