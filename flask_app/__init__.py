from flask import Flask 
from flask_bcrypt import Bcrypt
app = Flask(__name__)
app.secret_key = "dd022325-a18a-4c12-bd58-bbae2662aee1" #(when using session, good place to get one, powershell new-guid (use that code))
DATABASE = 'recipes_db'

bcrypt = Bcrypt(app)