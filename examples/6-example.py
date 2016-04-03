#forms
from flask import Flask, render_template #import Flask, Jinja2 rendering
from flask.ext.bootstrap import Bootstrap #import bootstrap - don't forget to pip install flask-bootstrap first
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

app = Flask(__name__) #Pass the __name__ argument to the Flask application constructor
app.config['SECRET_KEY'] = 'you_should_really_have_this_be_an_environment_variable'
bootstrap = Bootstrap(app)

class NameForm(Form):
    name = StringField('What would you like me to call you?', validators=[Required()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST']) #define the route for <server>/
def index(): #index function
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name=form.name.data
        form.name.data = ''
    return render_template('index.html', form=form, name=name)

@app.route('/<name>')
def user(name):
    return render_template('hello_bootstrap.html', name=name)

if __name__=='__main__': #only do the following if the script is executed directly skip if imported
    app.run() #start the integrated flask webserver
