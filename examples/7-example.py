#forms
from flask import Flask, render_template #import Flask, Jinja2 rendering
from flask.ext.bootstrap import Bootstrap #import bootstrap - don't forget to pip install flask-bootstrap first
from flask.ext.script import Manager #import flask-script
from flask.ext.sqlalchemy import SQLAlchemy
import os
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Required

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__) #Pass the __name__ argument to the Flask application constructor
manager = Manager(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SECRET_KEY'] = 'you_should_really_have_this_be_an_environment_variable'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

class NameForm(Form):
    name = StringField('What would you like me to call you?', validators=[Required()])
    location = SelectField("Location",choices=[('Home', 'Home'), ('Work', 'Work'), ('Class', 'Class')])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST']) #define the route for <server>/
def index(): #index function
    name = None
    form = NameForm()
    if form.validate_on_submit():
        existinguser=User.query.filter_by(username=form.name.data).first()
        if existinguser is None:
            name=form.name.data
            user=User(username=form.name.data, location=form.location.data)
            db.session.add(user)
        else:
            existinguser.username=form.name.data
            existinguser.location=form.location.data
            name=form.name.data
            db.session.commit()
    return render_template('index.html', form=form, name=name)

@app.route('/<name>')
def user(name):
    existinguser=existinguser=User.query.filter_by(username=name).first()
    return 'This user is at %s' % existinguser.location
    #return render_template('hello_bootstrap.html', name=name)

@app.route('/create_db')
def create_db():
    db.create_all()
    return '<h1>Database Created</h1>'

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    location = db.Column(db.String(64), nullable=True)

if __name__=='__main__': #only do the following if the script is executed directly skip if imported
    manager.run() #start the integrated flask webserver
