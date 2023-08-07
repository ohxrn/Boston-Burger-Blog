from flask_app import app
from flask import render_template, redirect, request, session
from flask import flash
from flask_app.models.user import User
from flask_app.models.sighting import Sighting
# from flask_app.models.dojo_ninja import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# ----------------NORMAL HOME ROUTEL----------------------------------------------


@app.route("/")
def user():
    return render_template("index.html")


@app.route("/create")
def create():
    return render_template("sightings.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')


# ----------------Route function for REGEX VAL----------------------------------------------
@app.route('/get_info', methods=['POST'])
def register():
    if not User.validate_user(request.form):
        # redirect to the route where the burger form is rendered.
        return redirect('/')

    # validate the form here ...
    # create the hash
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    # put the pw_hash into the data dictionary
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }

    # Call the save @classmethod on User
    user_id = User.save(data)
    # store user id into session
    session['user_id'] = user_id

    return redirect('/')


# ----------------Route function for if user already exists in DB----------------------------------------------

@app.route('/login', methods=['POST'])
def login():
    if not User.validate_user(request.form):
        # redirect to the route where the burger form is rendered.
        return redirect('/')
    # see if the username provided exists in the database
    data = {"email": request.form["email"]}
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("User email not in database")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Password incorrect")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id

    session['first_name'] = user_in_db.first_name

    # never render on a post!!!
    return redirect("/success")


@app.route('/success')
def successful():
    information = Sighting.get_both()
    return render_template("success.html", information=information)
