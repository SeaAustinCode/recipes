from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.model_recipe import DATABASE
from flask_app.models import model_recipe
from flask import flash, session
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__( self , data ):
        self.id = data['id'] #data in this is a dictionary --- data['id'] is how we are accessing the key of 'id' in the dictionary data and setting it to self.id
        self.first_name = data['first_name'] #DB Columns
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at'] #DB Columns
        self.updated_at = data['updated_at'] #DB Columns
    # Now we use class methods to query our database
    
    @classmethod
    def user_create(cls, data:dict): 
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);" #write the query in the workbench to test it 
        # database request
        user_id = connectToMySQL(DATABASE).query_db(query,data) #Target DB HERE city_id is variable name --> because insert query it'll return ID # of the row inserted
        return user_id
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(DATABASE).query_db(query) #THE RETURN IS A LIST OF DICTIONARIES
        # Create an empty list to append our instances of friends
        all_users = [] #becomes a list of instances
        # Iterate over the db results and create instances of users with cls. 
        for user in results: #for dictionary(city) in list of dictionaries (results line26) grab empty list (all_users line28) and append cls(city)
            all_users.append( cls(user) ) #[**Do NOT RETURN A LIST OF DICTIONARIES to HTML FOR THIS STACK -- RETURN A LIST OF INSTANCES]
        return all_users

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;" #adding a join here only adds data thats why it doesnt effect where it is currently in use
        result = connectToMySQL(DATABASE).query_db(query,data)
        if not result:
            return False # this stops it from trying to return a class instance of nothing.
        user = cls(result[0])
        return user

    @classmethod
    def get_one_by_email(cls, data:dict) -> list:
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return False

    @classmethod
    def get_one_user_and_its_recipes(cls, data):
        query = "SELECT * FROM users LEFT JOIN recipes ON users.id = recipes.user_id WHERE users.id = %(id)s;" #Select all from (table 1) left join (table 2) on (table 1 .id) = (table2.foreign key) where (table 1.id)
        result = connectToMySQL(DATABASE).query_db(query,data)

        user = cls(result[0])

        recipes = []
        for row in result:
            recipe_data = {
                **row,
                'id': row['recipes.id'],
                'created_at': row['recipes.created_at'],
                'updated_at': row['recipes.updated_at']
            }
            this_recipe = model_recipe.Recipe(recipe_data)
            recipes.append(this_recipe)
        user.recipes = recipes
        return user

    @classmethod
    def update_one(cls, data:dict) -> None:
        query = "UPDATE users SET first_name = %(first_name)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def delete_one(cls, data): #data is the dictionary
        query = "DELETE FROM users WHERE id = %(id)s;"# id is the keyname of the dictionary
        return connectToMySQL(DATABASE).query_db(query,data) #THE RETURN IS NOTHING

    @staticmethod
    def validate_registration(data:dict) -> bool:
        is_valid = True

        if len(data['first_name']) < 2:
            is_valid = False
            flash("first name is required", 'err_user_first_name')

        if len(data['last_name']) < 2:
            is_valid = False
            flash("last name is required", 'err_user_last_name')

        if len(data['email']) < 2:
            is_valid = False
            flash("email is required", 'err_user_email')
        elif not EMAIL_REGEX.match(data['email']): 
            is_valid = False
            flash("Invalid email address!")

        if len(data['password']) < 8:
            is_valid = False
            flash("password is required", 'err_user_password')

        if len(data['confirm_password']) < 8:
            is_valid = False
            flash("confirm password is required", 'err_user_confirm_password')
        elif data['password'] != data['confirm_password']:
            flash("Passwords do not match", 'err_user_confirm_password')
            is_valid = False

        return is_valid

    @staticmethod
    def validate_login(data:dict) -> bool:
        is_valid = True

        if len(data['email']) < 2:
            is_valid = False
            flash("email is required", 'login_err_user_email')

        if len(data['password']) < 8:
            is_valid = False
            flash("password is required", 'login_err_user_password')

        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!", 'login_err_user_email')
            is_valid = False

        return is_valid



