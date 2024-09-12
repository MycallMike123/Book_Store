from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Configure the SQLAlchemy part of the app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'

# Initialize the database
db = SQLAlchemy(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Import routes after initializing app and db
from bookstore import routes