from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
import re  # the regex module
# create a regular expression object that we'll use later

DATABASE = "sasquatches"


class Sighting:
    def __init__(self, data):
        self.id = data['id']
        self.location = data['location']
        self.what_happened = data['what_happened']
        self.sighting_date = data['sighting_date']
        self.how_many = data['how_many']
        self.user_id = data['user_id']

    @classmethod
    def save_recipe(cls, sight_data):
        query = """INSERT INTO sightings (location, what_happened, sighting_date, how_many, user_id)
                 VALUES (%(location)s,%(what_happened)s,%(sighting_date)s,%(how_many)s, %(user_id)s );
                """
        return connectToMySQL(DATABASE).query_db(query, sight_data)

    @classmethod
    def edit(cls, data_return):
        query = """ 
            UPDATE sightings
            SET location=%(location)s, what_happened=%(what_happened)s, sighting_date=%(sighting_date)s, how_many=%(how_many)s
            WHERE id=%(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data_return)
        return results

    # @classmethod
    # def get_one(cls, data4):
    #     query="""SELECT *
    #             FROM sightings
    #             JOIN users
    #             ON users.id=sightings.user_id
    #             WHERE sightings.id=(%(id)s);"""
    #     results1 = connectToMySQL(DATABASE).query_db(query, data4)
    #     print("HERE-------------------------------------------------------",results1)
    #     return results1

    @classmethod
    def delete(cls, data5):
        query = """DELETE FROM sightings
                    WHERE id=(%(id)s);
                    """
        results = connectToMySQL(DATABASE).query_db(query, data5)

    @classmethod
    def get_both(cls):
        query = """SELECT *
            FROM sightings
            JOIN users
            ON sightings.user_id=users.id;
                    """
        results = connectToMySQL(DATABASE).query_db(query)
        both_instances = []
        for row in results:
            this_row = cls(row)
            user_data = {
                **row,
                'id': row['user_id']
            }
            this_user = user.User(user_data)
            this_row.test = this_user
            both_instances.append(this_row)
        print("these are both instance:----------------------------------------------------->>>>>>>>>>",
              both_instances[0])
        return both_instances

    # @classmethod
    # def get_name(cls, data5):
    #     query = """SELECT *
    #         FROM users
    #         WHERE id = %(id)s;";
    #                 """

    #     results3 = connectToMySQL(DATABASE).query_db(query, data5)
    #     print("sdnf,sdnf,msmdf,.sdmf.sdmf,sfnsd,.fn,msfns,mfs,fbf",results3)
    #     return results3

    @classmethod
    def get_one(cls, data_id):
        query = "SELECT * FROM sightings WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data_id)
        return results

    @classmethod
    def update(cls, data):
        query = """
            UPDATE sightings
            SET first_name=%(fname)s, last_name=%(lname)s, email=%(occ)s
            WHERE id=%(id)s;
        """
        results = connectToMySQL('users_schema').query_db(query, data)
        return results

    @staticmethod
    def validate_sighting(boxes):
        is_valid = True  # we assume this is true
        if len(boxes['location']) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False
        if len(boxes['what_happened']) < 1:
            flash("You need to add a number!")
            is_valid = False
        if len(boxes['sighting_date']) < 1:
            flash("you need to have a valid date!")
            is_valid = False
        if len(boxes['how_many']) < 1:
            flash("you need to have at least one sasquatch!")
            is_valid = False
        if len(boxes['how_many']) == 0:
            flash("you need to have at least one sasquatch!")
            is_valid = False
        return is_valid
