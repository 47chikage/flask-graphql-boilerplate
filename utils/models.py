from flask import Flask,request,render_template,jsonify,redirect,url_for,flash,abort,session
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin,AdminIndexView,expose
from flask_admin.contrib.sqla import ModelView
import json
from functools import wraps

#app init
app = Flask('boilerplate')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///records.db'
db = SQLAlchemy(app)
app.secret_key = 'your_secret_key'

#login tools
def load_user(username):
    return Person.query.filter_by(username=username).first()

def current_user():
    if 'user' in session:
        return session['user']
    return None

def login_user(user):
    user={key:str(value) for key,value in user.__dict__.items() if key!='_sa_instance_state'}
    with app.app_context():session['user']=user

def logout_user():
    with app.app_context():session['user']=None

def check_login(username,password):
    user=load_user(username)
    if user is not None:
        if password==user.password:
            login_user(user)
            return True
    return False
#use it as decorator, see in main
def login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return decorated_view


# Define SQLAlchemy models
class Person(db.Model):
    username=db.Column(db.String(100),primary_key=True)
    password=db.Column(db.String(100))
    role=db.Column(db.String(100))

#admin tools
class AdminModelView(ModelView):
    def is_accessible(self):
        return True
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))
    
#customize your admin view function
class AdminHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        user=current_user()
        if user and user['role']=='admin':
                return self.render('admin/index.html')
        return redirect(url_for('login'))
        

admin = Admin(app,name='admin', template_mode='bootstrap3', index_view=AdminHomeView())
admin.add_view(AdminModelView(Person, db.session))

#run once to create database
"""with app.app_context():
    db.create_all()"""