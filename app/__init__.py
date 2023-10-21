#Flask
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisasecretkey'
from app import routes

