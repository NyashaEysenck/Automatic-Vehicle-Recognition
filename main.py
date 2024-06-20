"""
Main entry point for the Flask web application.

This module creates an instance of the Flask application, sets up the application
context to ensure the database tables are created, and runs the application in
debug mode.

Modules:
    web_application: Custom module containing the Flask application factory and database instance.
"""
from web_application import create_app, DB

APP = create_app()

if __name__ == "__main__":
    APP.run(debug=True)
