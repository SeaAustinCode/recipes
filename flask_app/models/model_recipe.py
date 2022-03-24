from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import model_user

DATABASE = 'recipes_db'

class Recipe:
    def __init__( self , data ):
        self.id = data['id'] #data in this is a dictionary --- data['id'] is how we are accessing the key of 'id' in the dictionary data and setting it to self.id
        self.name = data['name'] #DB Columns
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made_on = data['date_made_on']
        self.under_30_mins = data['under_30_mins']
        self.user_id = data['user_id']
        self.created_at = data['created_at'] #DB Columns
        self.updated_at = data['updated_at'] #DB Columns
    # Now we use class methods to query our database
    
    @classmethod
    def create(cls, data:dict): 
        query = "INSERT INTO recipes (name, description, instructions, date_made_on, under_30_mins, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made_on)s, %(under_30_mins)s, %(user_id)s);" #write the query in the workbench to test it 
        # database request
        recipe_id = connectToMySQL(DATABASE).query_db(query,data) #Target DB HERE city_id is variable name --> because insert query it'll return ID # of the row inserted
        return recipe_id
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(DATABASE).query_db(query) #THE RETURN IS A LIST OF DICTIONARIES
        # Create an empty list to append our instances of friends
        all_recipes = [] #becomes a list of instances
        # Iterate over the db results and create instances of recipe with cls. 
        for recipe in results: #for dictionary(city) in list of dictionaries (results line22) grab empty list (all_cities line24) and append cls(city)
            all_recipes.append( cls(recipe) ) #[**Do NOT RETURN A LIST OF DICTIONARIES to HTML FOR THIS STACK -- RETURN A LIST OF INSTANCES]
        return all_recipes

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;" #adding a join here only adds data thats why it doesnt effect where it is currently in use
        result = connectToMySQL(DATABASE).query_db(query,data)
        if not result:
            return False # this stops it from trying to return a class instance of nothing.
        recipe = cls(result[0])
        return recipe

    @classmethod
    def update(cls, data):
        query = """UPDATE recipes SET
                name=%(name)s,
                description=%(description)s,
                instructions=%(instructions)s,
                date_made_on=%(date_made_on)s,
                under_30_mins=%(under_30_mins)s,
                updated_at=NOW()
                WHERE recipes.id = %(id)s;"""
        result = connectToMySQL(DATABASE).query_db(query,data)
        return result

    @classmethod
    def delete_one(cls, data): #data is the dictionary
        query = "DELETE FROM recipes WHERE id = %(id)s;"# id is the keyname of the dictionary
        return connectToMySQL(DATABASE).query_db(query,data) #THE RETURN IS NOTHING