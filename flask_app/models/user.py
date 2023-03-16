# CONNECT DB
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    # CREATE DB variable
    DB = "login_reg"
    # MATCH init to DB fields
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

# CREATE (match DB)
    @classmethod
    def save(cls,data):
        query = """
                INSERT INTO users (first_name,last_name,email,password) 
                VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s);
            """
        return connectToMySQL(cls.DB).query_db(query,data)

# READ (all, id, and email)
    @classmethod
    def get_all(cls):
        query = """
                SELECT * FROM users;
                """
        results = connectToMySQL(cls.DB).query_db(query)
        users = []
        for row in results:
            users.append( cls(row))
        return users

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def get_by_email(cls,data):
        query = """
                SELECT * FROM users 
                WHERE email = %(email)s;
                """
        results = connectToMySQL(cls.DB).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
# UPDATE

# DELETE

# VALIDATE (import flash, re, REGEX)
    @staticmethod
    def validate_register(user):
        is_valid = True
        query = """
                SELECT * FROM users WHERE email = %(email)s;
                """
        results = connectToMySQL(User.DB).query_db(query,user)
        if len(results) >= 1:
            flash("Email already in use","register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Email not valid","register")
            is_valid = False
        if len(user['first_name']) < 3:
            flash("First name: needs at least 3 characters","register")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name: needs at least 3 characters","register")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password: needs at least 8 characters","register")
            is_valid = False
        if user['password'] != user['confirm']:
            flash("Password does not match","register")
            is_valid = False
        return is_valid