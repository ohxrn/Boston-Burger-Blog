from flask_app import app
from flask_app.controllers import the_user
from flask_app.controllers import the_sightings


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=9000)
