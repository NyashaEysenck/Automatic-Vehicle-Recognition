"""
Initialization module for the Flask application.

This module sets up the Flask application, configures logging, initializes
extensions such as SQLAlchemy, Flask-Mail, and Flask-Login, and sets up the
database with an initial user. It also registers all the necessary blueprints
for the application routes.

Modules:
    logging: Provides logging functionality.
    os: Provides a way to use operating system dependent functionality.
    flask: The core module for Flask web application framework.
    flask_sqlalchemy: SQLAlchemy integration for Flask.
    flask_login: Provides user session management for Flask.
    werkzeug.security: Provides password hashing utilities.
    flask_mail: Provides email sending capabilities for Flask.
    itsdangerous: Provides security utilities for generating tokens.
    dotenv: Loads environment variables from a .env file.

Functions:
    create_app: Creates and configures an instance of the Flask application.
"""

import logging
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask and database instances
APP = Flask(__name__)

logging.basicConfig(filename='trail.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

logging.debug("This is a test")

DB = SQLAlchemy()
MAIL = Mail()

# Token serializer setup
SERIALIZER = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))

def create_app(config_name='development'):
    """
    Creates and configures an instance of the Flask application.

    Args:
        config_name (str): The configuration name to use. Can be 'development' or 'production'.

    Returns:
        Flask: The configured Flask application instance.
    """
    from .config import config

    # Configure Flask app
    APP.config.from_object(config[config_name])

    # Initialize extensions
    DB.init_app(APP)
    MAIL.init_app(APP)

    # Model import
    from .models import Guard

    # Create database tables if they don't exist
    with APP.app_context():
        DB.create_all()

        # Create an initial user (modify as needed)
        if not Guard.query.filter_by(username='Supervisor').first():
            initial_user = Guard(
                username='Supervisor',
                password=generate_password_hash(
                    'RandomPassword123', method='scrypt', salt_length=16),
                email=os.getenv('MAIL_USERNAME'),
                supervisor=True,
                suspended=False
            )
            DB.session.add(initial_user)
            DB.session.commit()

    # Import and register Blueprints (organize routes)
    from .routes.auth import auth
    from .routes.system import system
    from .routes.client_routes import client_routes
    from .routes.home_routes import home_routes
    from .routes.vehicle_routes import vehicle_routes
    from .routes.other import help_routes, settings_routes
    from .routes.forgot import forgot
    from .routes.admin import accounts

    APP.register_blueprint(home_routes, url_prefix='/')
    APP.register_blueprint(vehicle_routes, url_prefix='/')
    APP.register_blueprint(client_routes, url_prefix='/')
    APP.register_blueprint(auth, url_prefix='/')
    APP.register_blueprint(system, url_prefix='/')
    APP.register_blueprint(help_routes, url_prefix='/')
    APP.register_blueprint(settings_routes, url_prefix='/')
    APP.register_blueprint(accounts, url_prefix='/')
    APP.register_blueprint(forgot, url_prefix='/')

    # Configure Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(APP)

    @login_manager.user_loader
    def load_user(guard_id):
        return Guard.query.get(int(guard_id))

    return APP

if __name__ == '__main__':
    None
