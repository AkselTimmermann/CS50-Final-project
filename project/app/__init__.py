from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__) # creates the flask application
app.config['SECRET_KEY'] = 'lEk0wS2azX' # securely signs cookies to protect against attacks
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # SQLite database

db = SQLAlchemy(app) # links flask app with SQLALCHEMY extension
migrate = Migrate(app, db)
login_manager = LoginManager(app) # simplifies user sessions like login in and out. provides @login_required
login_manager.login_view = 'login' # if user not logged in. redirect to login.html

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from app import routes
from app.models import User
