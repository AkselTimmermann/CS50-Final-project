from app import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin): # db.model links the user class to a table in the database. UserMixin provides useful methods like is_authenticated
    id = db.Column(db.Integer, primary_key=True) # unique identifier for each user
    username = db.Column(db.String(20), unique=True, nullable=False) # username field, must be unique
    email = db.Column(db.String(120), unique=True, nullable=False) # email field, must be unique
    password = db.Column(db.String(60), nullable=False) #password field, HASHING LATER

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer, nullable=False) #duration in minutes
    distance = db.Column(db.Float, nullable=True) #duration in kilometers
    calories = db.Column(db.Integer, nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text, nullable=True)

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #links to the user
    month = db.Column(db.String(7), nullable=False) # yyyy-mm for simplicity
    yoga_session = db.Column(db.Integer, nullable=False, default=0)
    running_distance = db.Column(db.Float, nullable=False, default=0.0)
    weightlifting_session = db.Column(db.Integer, nullable=False, default=0)



