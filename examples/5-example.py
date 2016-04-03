from flask import Flask, render_template #import Flask, Jinja2 rendering
from flask.ext.bootstrap import Bootstrap #import bootstrap - don't forget to pip install flask-bootstrap first
app = Flask(__name__) #Pass the __name__ argument to the Flask application constructor
bootstrap = Bootstrap(app)

@app.route('/') #define the route for <server>/
def index(): #index function
    return render_template('hello_bootstrap.html')

@app.route('/<name>')
def user(name):
    return render_template('hello_bootstrap.html', name=name)

if __name__=='__main__': #only do the following if the script is executed directly skip if imported
    app.run() #start the integrated flask webserver
