from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField, SelectField, DateField, TimeField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange, Optional, ValidationError

class WorkoutForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()]) # Date picker
    activity_type = SelectField(
        'Activity Type',
        choices=[('Yoga', 'Yoga'), ('Running', 'Running'), ('Weightlifting', 'Weightlifting')],
        validators=[DataRequired()]
    )
    duration = IntegerField('Duration', validators=[DataRequired(), NumberRange(min=0, message="Must be a positive number")])
    distance = FloatField('Distance', validators=[Optional(), NumberRange(min=0)], render_kw={"placeholder": "Only for running (km)"})
    calories = IntegerField('Calories Burned', validators=[Optional(), NumberRange(min=0)], render_kw={"placeholder": "Only for running"})
    submit = SubmitField('Log Workout')

    # custom validation for distance and calories based on activity_type
    def validate_distance(self, field):
        if self.activity_type.data == 'Running' and not field.data:
            raise ValidationError("Distance is required for running activities.")

    def validate_calories(self, field):
        if self.activity_type.data == 'Running' and not field.data:
            raise ValidationError("Calories burned is required for running activities.")

class GoalForm(FlaskForm):
    yoga_session = IntegerField('Yoga Sessions', validators=[DataRequired(), NumberRange(min=0, message="Must be a positive number")])
    running_distance = FloatField('Running Distance', validators=[DataRequired(), NumberRange(min=0, message="Must be a positive number")])
    weightlifting_session = IntegerField('Weightlifting Sessions', validators=[DataRequired(), NumberRange(min=0, message="Must be a positive number")])
    submit = SubmitField('Set monthly goal')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message="Enter a valid email address")]) # field for email, input is required
    password = PasswordField('Password', validators=[DataRequired()]) # field for password,
    submit = SubmitField('Login') # submit field

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()]) # Field for username, input is required
    email = StringField('Email', validators=[DataRequired(), Email(message="Enter a valid email address")])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')]) # field for confirmation of password
    submit = SubmitField('Sign Up')
