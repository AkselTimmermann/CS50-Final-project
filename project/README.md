# Workout logger
#### VIDEO DEMO: <URL HERE>
#### Description

This website makes it possible for the user to log and save their workout. There are three different workouts: weightlifting, running and yoga. When a user has done a workout they choose the correct one and then a new form pops up where they can enter the duration. If running is chosen "Distance" also pops up.
There is also a "Monthly goal" form where the user can log, you guessed it, their monthly goal.
The user has to make an account and log in, otherwise it can't be saved in the database.

_init_.py is where i initialize the flask app using the (_name_). I also set up the database and application settings like the secret key to make it more secure. Login_manager should simplify the login-logout process and redirects to the login.html if user is not logged in. routes (where all my URL's are) is imported at the bottom of this file because the app = flask(_name_) is created in this file and the routes needs to be aware of the app object to proberly function. They need to be linked together.

forms.py contains a basic login form, i dont need anything fancy it's just to make sure the user logs in so he can get all the features when using my website. I use Flask-wtf so i can get extensions that provides useful features that should make it easier and more simple to make web forms. By that i mean i need to do less in the .html files that include forms.

routes.py has all the BACK-END python code for the different URL's on my website. I felt it would be easier to seperate it from all the other coding i made.

models.py is where i'm adding users into the database. Before i've only used sqlite3 which is a easier way to work in the database but i decided to challenge myself and use SQLAlchemy. Another reason is that i expect this to be the way to do it moving forward.

I had trouble making the database with flask so i had to do it manually. Therefore i made the file "create_db.py".
