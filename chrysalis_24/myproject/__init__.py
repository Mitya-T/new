#__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap


login_manager = LoginManager() # object that simplifies the login procedures etc


app = Flask(__name__)

# Because we have a FORM we have to configure a secret key
app.config['SECRET_KEY'] = 'mysecretkey'
Bootstrap(app)


#~~~~~~~~~~~~~~~~~ SQL DATABASE SECTION ~~~~~~~~~~~~~~~~~

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

login_manager.init_app(app) # initiate the app to manage login
login_manager.login_view = 'login'
