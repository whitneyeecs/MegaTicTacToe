#forms
from flask import Flask, jsonify, render_template, flash, url_for, request, redirect #import Flask, Jinja2 rendering
from flask.ext.bootstrap import Bootstrap #import bootstrap - don't forget to pip install flask-bootstrap first
from flask.ext.script import Manager #import flask-script
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField, BooleanField, PasswordField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from flask.ext.login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__) #Pass the __name__ argument to the Flask application constructor
manager = Manager(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SECRET_KEY'] = 'you_should_really_have_this_be_an_environment_variable'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'



class NameForm(Form):
    location = SelectField("Location",choices=[('Home', 'Home'), ('Work', 'Work'), ('Class', 'Class')])
    submit = SubmitField('Submit')

class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class RegistrationForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                           Email()])
    username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    password = PasswordField('Password', validators=[
        Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email taken')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data, location='new_user')
        db.session.add(user)
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/', methods=['GET', 'POST']) #define the route for <server>/
@login_required
def index(): #index function
    form = NameForm()
    if form.validate_on_submit():
            current_user.location=form.location.data
            db.session.add(current_user)
            flash('Location updated.')
    otherusers=User.query.all()
    return render_template('index.html', form=form, otherusers=otherusers)

@app.route('/<name>')
def user(name):
    existinguser=existinguser=User.query.filter_by(username=name).first()
    return 'This user is at %s' % existinguser.location
    #return render_template('hello_bootstrap.html', name=name)

@app.route('/db/create_db')
def create_db():
    db.create_all()
    return '<h1>Database Created</h1>'

@app.route('/db/drop_db')
def drop_db():
    db.drop_all()
    return '<h1>Database Cleared</h1>'

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    location = db.Column(db.String(64), nullable=True)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__=='__main__': #only do the following if the script is executed directly skip if imported
    manager.run() #start the integrated flask webserver
