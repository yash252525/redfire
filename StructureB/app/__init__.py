from flask import Flask
from jinja2 import StrictUndefined
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

with app.app_context():
    from . import views
