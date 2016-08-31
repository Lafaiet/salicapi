from flask import Flask
from general_config import ENVIRONMENT

app = Flask(__name__)
app.config.from_pyfile(ENVIRONMENT)
