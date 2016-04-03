#introducting templates
from flask import Flask, render_template #import Flask, Jinja2 Template rendering
app = Flask(__name__) #Pass the __name__ argument to the Flask application constructor

@app.route('/') #define the route for <server>/
def index(): #index funciton
    return '<h1>Hello 390!</h1>' #return this message

@app.route('/<name>')
def user(name):
    return render_template('hello.html', name=name) #instead of sending message back, render the template called ./templates.html, passing the name variable.

if __name__=='__main__': #only do the following if the script is executed directly skip if imported
    app.run() #start the integrated flask webserver
