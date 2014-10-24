from flask_appconfig import AppConfig
from flask import Flask, render_template, request, Response
from flask_bootstrap import Bootstrap

from datetime import datetime
import time
import os
import subprocess
from functools import wraps
import numpy
import random
import json

auth = {"user":"emboi","password":"emboi"}

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == auth["user"] and password == auth["password"]

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

def create_app(configfile=None):
	app = Flask(__name__)
	AppConfig(app, configfile)
	Bootstrap(app)

	@app.route('/')
	@requires_auth
	def showCounters():
		return "Hello there, this will be a transport management app"
		#return render_template('bars.html',collections = collections, stats = stats, statsKeys = statsKeys, astros = astros)

	


	return app

if __name__ == '__main__':
    create_app().run(host="0.0.0.0",debug=True)
