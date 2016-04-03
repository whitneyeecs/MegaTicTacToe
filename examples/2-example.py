#flask with a name route
from flask import Flask #import Flask
app = Flask(__name__) #Pass the __name__ argument to the Flask application constructor

@app.route('/') #define the route for <server>/
def index(): #index funciton
    return '<h1>Hello 390!</h1>' #return this message

@app.route('/<name>')
def user(name):
    return '<h1> Hello %s, it&#39s nice to see you.' % name

if __name__=='__main__': #only do the following if the script is executed directly skip if imported
    app.run() #start the integrated flask webserver
