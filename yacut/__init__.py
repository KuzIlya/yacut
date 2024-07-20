from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from settings import Config

app = Flask(__name__)
app.config.from_object(Config)
app.json.ensure_ascii

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from . import api_views, cli_commands, errors_handlers, views
