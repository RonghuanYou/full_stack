from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app

from flask import flash
from flask_bcrypt import Bcrypt
import re
from flask_app.models import recipe

bcrypt = Bcrypt(app)


class User:
    # good for reuse
    schema = "recipes_schema"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []

    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO users(first_name, last_name, email, password)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        return connectToMySQL(cls.schema).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.schema).query_db(query)

        all_users = []
        for row in results:
            all_users.append(cls(row))
        return all_users

    @classmethod
    def get_one(cls, data):
        query = """
            SELECT * FROM users LEFT JOIN recipes ON users.id = recipes.user_id
            WHERE users.id = %(id)s;
        """
        results = connectToMySQL(cls.schema).query_db(query, data)
        user = cls(results[0])

        for row in results:
            row_data = {
                "id": row['recipes.id'],
                "name": row['name'],
                "description": row['description'],
                "instruction": row['instruction'],
                "date_made": row['date_made'],
                "under_30_mins": row['under_30_mins'],
                "created_at": row['recipes.created_at'],
                "updated_at": row['recipes.updated_at']
            }

            user.recipes.append(recipe.Recipe(row_data))
        return user



    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.schema).query_db(query, data)

        if len(results) < 1:
            return False

        # if nothing in db, we can't return it
        return cls(results[0])

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.schema).query_db(query, data)

        if len(results) < 1:
            return False
        return cls(results[0])

    @staticmethod
    def register_validate(post_data):
        is_valid = True
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        # attributes: first_name, last_name, email, password, comfirm_password
        if len(post_data['first_name']) < 2:
            flash("First name must be at least 2 characters.")
            is_valid = False
        if len(post_data['last_name']) < 2:
            flash("Last name must be at least 2 characters.")
            is_valid = False

        # check email format
        # check if email already exists in db
        if not EMAIL_REGEX.match(post_data['email']):
            flash("Email is not valid!")
            is_valid = False
        elif User.get_by_email({"email": post_data['email']}):
            flash("Email is already in use")
            is_valid = False

        if len(post_data['password']) < 8:
            flash("Password must be at least 8 characters")
            is_valid = False
        elif post_data['password'] != post_data['confirm_password']:
            flash("Two passwords don't match!")
            is_valid = False
        return is_valid


    @staticmethod
    def login_validate(post_data):
        # if email doesn't exist in db, it's invalid
        # if input password doesn't match pass in db, it's invalid
        # user: object type
        user = User.get_by_email({"email": post_data['email']})
        if not user:
            flash("Invalid account")
            return False

        #  post_data['password'] will be hashed automatically
        if not bcrypt.check_password_hash(user.password, post_data['password']):
            flash("Invalid password")
            return False

        return True
