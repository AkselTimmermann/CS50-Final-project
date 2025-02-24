from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, GoalForm, WorkoutForm
from app.models import User, Goal, Workout
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
from sqlalchemy import func, extract

@app.route("/", methods=['GET', 'POST'])
@login_required
def home():
    goal_form = GoalForm()
    workout_form = WorkoutForm()
    current_month = datetime.utcnow().strftime("%Y-%m") # Get the current month in "YYYY-MM" format

    # Check if a goal for the month already exist for the user
    existing_goal = Goal.query.filter_by(user_id=current_user.id, month=current_month).first()

    if existing_goal and request.method == 'GET':
        # pre-fill the submit form with existing data if a GET request
        goal_form.yoga_session.data = existing_goal.yoga_session
        goal_form.running_distance.data = existing_goal.running_distance
        goal_form.weightlifting_session.data = existing_goal.weightlifting_session

    # handle form submission
    if goal_form.validate_on_submit(): # checks if the form is submitted and valid
        if existing_goal:
            # update the existing goal if it already exists
            existing_goal.yoga_session = goal_form.yoga_session.data
            existing_goal.running_distance = goal_form.running_distance.data
            existing_goal.weightlifting_session = goal_form.weightlifting_session.data
            flash('Monthly goal updated successfully!', 'success')
        else:
            # create a new goal if none exists
            new_goal = Goal(
                user_id=current_user.id,
                month=current_month,
                yoga_session=goal_form.yoga_session.data,
                running_distance=goal_form.running_distance.data,
                weightlifting_session=goal_form.weightlifting_session.data,
            )
            db.session.add(new_goal)
            flash('Monthly goal set successfully!', 'success')

        db.session.commit()
        return redirect(url_for('home'))

    # Handle workout logging/Form submitting
    if workout_form.validate_on_submit(): # Create new workout
        new_workout = Workout(
            user_id=current_user.id,
            date=workout_form.date.data,
            activity_type=workout_form.activity_type.data,
            duration=workout_form.duration.data,
            distance=workout_form.distance.data if workout_form.activity_type.data == 'Running' else None,
            calories=workout_form.calories.data if workout_form.activity_type.data == 'Running' else None
        )

        try:
            db.session.add(new_workout)
            db.session.commit()
            flash('Workout logged successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Failed to log workout.', 'danger')

        flash('Workout logged successfully!', 'success')
        return redirect(url_for('home'))

    # workout history logic - seperate by activity
    activity_types = ["Yoga", "Running", "Weightlifting"]
    monthly_activity_summary = {}
    total_activity_summary = {}

    for activity in activity_types:
        # monthly summary for each activity
        datetime_month = datetime.strptime(current_month, "%Y-%m")

        # Calculate the start and end of the current month
        start_of_month = datetime_month.replace(day=1)
        end_of_month = (start_of_month + timedelta(days=31)).replace(day=1) - timedelta(seconds=1)

        monthly_workouts = Workout.query.filter(
            Workout.user_id == current_user.id,
            Workout.activity_type == activity,
            Workout.date >= start_of_month,
            Workout.date <= end_of_month
        ).all()

        monthly_activity_summary[activity] = {
            "count": len(monthly_workouts),
            "duration_hours": sum(workout.duration or 0 for workout in monthly_workouts) / 60, #convert minutes to hours
            "running_distance": sum(workout.distance or 0 for workout in monthly_workouts if activity == 'Running')
        }

        # all time summary for each activity
        all_time_workouts = Workout.query.filter(Workout.user_id == current_user.id, Workout.activity_type == activity).all()
        total_activity_summary[activity] = {
            "count": len(all_time_workouts),
            "duration_hours": sum(workout.duration or 0 for workout in all_time_workouts) / 60, #convert minutes to hours
            "running_distance": sum(workout.distance or 0 for workout in all_time_workouts if activity == 'Running')
        }

    return render_template(
        'home.html',
        goal_form=goal_form,
        workout_form=workout_form,
        monthly_activity_summary=monthly_activity_summary,
        total_activity_summary=total_activity_summary
    )


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit(): # checks if it's a POST request and if it's valid
        user = User.query.filter_by(email=form.email.data).first() # searches user table for email that matches the one provided in the login form. returns None if user doesn't exist

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))

        else:
            flash('Login unsuccessful. please check email and password', 'danger')

    # if it's a GET request, show login form. because form.validate_on_submit is false
    return render_template('login.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out!', 'info')
    return redirect(url_for('login'))


@app.route("/register", methods=['GET', 'POST'])
def register():

    form = RegistrationForm()

    if form.validate_on_submit(): # if POST request and it's valid

        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('An account with that email already exists', 'danger')
            return render_template('register.html', form=form)

        hashed_password = generate_password_hash(form.password.data) # hash the password

        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password) # Create new user

        # add new user in the site.db database
        db.session.add(new_user)
        db.session.commit()

        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login')) # Redirect to login page after registration

    # if its get request of the form is invalid, render the registration page again
    return render_template('register.html', form=form)



