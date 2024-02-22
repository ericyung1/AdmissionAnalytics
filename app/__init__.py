# app/__init__.py
from flask import Flask

# Initialize the Flask application
app = Flask(__name__)

# Import the views module, which contains your routes
from app import views  # Import the views module after creating the app

# Register the blueprint
app.register_blueprint(views.bp)
