from flask import Flask
from flask import render_template
from flask_turbolinks import turbolinks

app = Flask(__name__)

turbolinks(app)

from app import views