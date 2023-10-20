from flask import Flask
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

import routes

#import timefunctions

#app.jinja_env.globals.update(timefunctions=timefunctions)