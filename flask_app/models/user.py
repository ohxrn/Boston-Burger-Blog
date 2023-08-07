from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import sighting
import re  # the regex module
# create a regular expression object that we'll use later


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
DATABASE = "sasquatches"


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']


# ----------A GET ALL FUNCTION-------------------------------------------------------------

    @classmethod
    def get_user(cls):
        query = """SELECT *
                   FROM users;"""
        results = connectToMySQL(DATABASE).query_db(query)
        user_list = []
        for row in results:
            user_list.append(cls(row))
        return user_list

# -------------------------REGEX---------------------------------------------

    @staticmethod
    def validate_user(user):
        print(user)
        is_valid = True
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!", 'email')
            is_valid = False
        if len(user['password']) == " ":
            flash("Enter input for password.")
            is_valid = False
        # if len(user['first_name']) < 2:
        #     flash("First name must be at least 3 characters.")
        #     is_valid = False
        # if len(user['last_name']) < 2:
        #     flash("Last name must be at least 3 characters.")
        #     is_valid = False
        if len(user['email']) == 0:
            flash("Need to enter an email.")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password needs to be at least 8 characters")
            is_valid = False
        return is_valid


# -------------------------Function for checking if user exists in DB---------------------------------------------

    @classmethod
    def get_by_email(cls, data):
        query = """SELECT * 
        FROM users 
        WHERE email = %(email)s;"""
        result = connectToMySQL(DATABASE).query_db(query, data)

        print(result)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_by_final(cls, data1):
        query = """SELECT *
                   FROM users
                   WHERE id=%(id)s;"""
        results = connectToMySQL(DATABASE).query_db(query, data1)
        return results

# ---------SAVE FUNCTION-------------------------------------------------------------

    @classmethod
    def save(cls, data):
        query = """INSERT INTO users (first_name, last_name, email, password)
                 VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);
                """
        return connectToMySQL(DATABASE).query_db(query, data)

# ---------SAVE FUNCTION-------------------------------------------------------------
