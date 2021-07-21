from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app

from flask import flash
from flask_bcrypt import Bcrypt
import re
from flask_app.models import user

bcrypt = Bcrypt(app)


class Recipe:
    # good for reuse
    schema = "recipes_schema"

    def __init__(self, data):
        self.id = data['id']
        # create user object 
        if 'user_id' in data:
            self.user_id = user.User.get_one({"id": data['user_id']})
        self.name = data['name']
        self.description = data['description']
        self.instruction = data['instruction']
        self.date_made = data['date_made']
        self.under_30_mins = data['under_30_mins']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO recipes(name, user_id, description, instruction, date_made, under_30_mins)
            VALUES (%(name)s, %(user_id)s,%(description)s, %(instruction)s, %(date_made)s, %(under_30_mins)s);
        """
        return connectToMySQL(cls.schema).query_db(query, data)


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(cls.schema).query_db(query)

        all_users = []
        for row in results:
            all_users.append(cls(row))
        return all_users

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL(cls.schema).query_db(query, data)
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = """
            UPDATE recipes SET name = %(name)s, description = %(description)s, instruction = %(instruction)s, 
            date_made = %(date_made)s, under_30_mins = %(under_30_mins)s WHERE id = %(id)s;
        """        
        return connectToMySQL(cls.schema).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(cls.schema).query_db(query, data)


    @staticmethod
    def recipe_validate(post_data):
        is_valid = True

        # attributes: name, description, instruction, date_made, under_30_mins
        if len(post_data['name']) < 3:
            flash("Recipe name must be at least 3 characters.")
            is_valid = False

        if len(post_data['description']) < 3:
            flash("Recipe description must be at least 3 characters.")
            is_valid = False

        if len(post_data['instruction']) < 3:
            flash("Recipe instruction must be at least 3 characters.")
            is_valid = False

        return is_valid

