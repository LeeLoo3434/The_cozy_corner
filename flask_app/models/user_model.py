from flask import flash, session
from flask_app.config.mysqlconnection import connectToMySQL
import re

DATABASE = 'my_cozy_corner'

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.user_name = data['user_name']
        self.pronouns = data['pronouns']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.events = []

    def __repr__(self):
        return f'<User: {self.user_name}>'

    @staticmethod
    def validate_registration(form):
        is_valid = True
        if len(form['user_name']) < 2:
            flash('username must be at least two characters', 'user_name')
            is_valid = False
        if len(form['pronouns']) < 2:
            flash('pronouns plz')
            is_valid = False
        if not EMAIL_REGEX.match(form['email']):
            flash("Invalid email address!", 'email')
            is_valid = False
        if len(form['password']) < 8:
            flash('Password must be at least eight characters', 'password')
            is_valid = False
        else:
            if form['password'] != form['confirm_password']:
                flash('passwords must match', 'confirm_password')
                is_valid = False
        return is_valid

    @staticmethod
    def validate_login(form):
        is_valid = True
        if not EMAIL_REGEX.match(form['email']):
            flash("Invalid email address!", 'log_email')
            is_valid = False
        if len(form['password']) < 8:
            flash('Password must be at least eight characters', 'log_password')
            is_valid = False
        return is_valid

    # find by email
    @classmethod
    def find_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email= %(email)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) > 0:
            return User(results[0])
        return None

        # create a user
    @classmethod
    def save(cls, data):
        # dont need created_at or created_at
        query = 'INSERT INTO users (user_name, email, pronouns, password) VALUES (%(user_name)s, %(email)s,%(pronouns)s, %(password)s);'
        user_id = connectToMySQL(DATABASE).query_db(query, data)
        return user_id

    # find one user by id

    @classmethod
    def find_by_id(cls, data):
        query = 'SELECT * from users WHERE id = %(id)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) > 0:
            return User(results[0])
        return None
