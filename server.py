from flask_app import app
from flask_app.controllers import controller_recipe, controller_user, controller_routes


# KEEP THIS AT THE BOTTOM 
if __name__=="__main__":
    app.run(debug=True)