from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import model_user, model_recipe
from flask_app.models.model_user import User
from flask_app.models.model_recipe import Recipe

@app.route('/')
def index():
    if 'uuid' in session:
        return redirect('/dashboard')

    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'uuid' not in session:
        return redirect('/')
    user = User.get_one({"id":session["uuid"]}) #variable user = class(User)function to select(give it the value of the user that is logged in)
    return render_template('dashboard.html', user=user, recipes=Recipe.get_all())

@app.route('/')
def all_users():
    all_users = model_user.User.get_all() #model_user = filename, User = class get all = function
    return render_template('index.html', all_users=all_users) ## this is rendering the homepage