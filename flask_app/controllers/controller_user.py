from flask_app import app, bcrypt
from flask import render_template, redirect, request, session, flash
from flask_app.models.model_user import User
from flask_app.models import model_user


@app.route('/user/new')
def user_new():
    return redirect('/')

@app.route('/user/login', methods=['post'])
def user_login():
    #validate
    if not model_user.User.validate_login(request.form):
        return redirect('/')
    user_in_db = model_user.User.get_one_by_email({"email":request.form['email']}) #key of email and value input of request.form['email']
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['uuid'] = user_in_db.id
    # never render on a post!!!
    return redirect("/dashboard")

@app.route('/user/create', methods=['post']) #action route ---> returns redirect
def user_create():
    #validate
    if not model_user.User.validate_registration(request.form):
        return redirect('/')
    #hash
    hash_pw = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password': hash_pw
    }
    #create
    id = model_user.User.user_create(data)
    session['uuid'] = id
    return redirect("/dashboard")

@app.route('/user/<int:id>') #individual user pages
def user_show(id):
    data = {
        'id': id #'id' is the keyname which must match the name of the keyname passed in the classmethod the second id is the variable from def dojo_delete
    }
    user = User.get_one_user_and_its_recipes(data)
    return render_template('dashboard.html', user=user)

@app.route('/user/edit')
def user_edit():
    pass #probably need to change this 

@app.route('/user/update')
def user_update():
    pass #probably need to change this 

@app.route('/user/<int:id>/delete')
def user_delete(id):
    data = {
        'id': id #'id' is the keyname which must match the name of the keyname passed in the classmethod the second id is the variable from def user_delete
    }
    User.delete_one(data) # instead of doing the above you can pass dictionary directly in here User.delete_one({'id': id})
    return redirect('/') 

@app.route('/user/logout')
def user_logout(): 
    session.pop('uuid')
    return redirect('/')

# @app.route('/')
# def index():
#     context = {
#         'all_users': User.get_all(),
#         #'all_players': Player.get_all(),
#     }
#     #Variable = Classname.methodname()
#     return render_template('login.html', **context) #**context takes in all the items below it so no need to write out individ 
#     #return render_template('all_cities', 'all_players' etc etc)

