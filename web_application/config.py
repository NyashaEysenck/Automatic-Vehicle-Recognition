
import os

class Config:
    """
    Base configuration class for the Flask application.
    
    Attributes:
        SECRET_KEY (str): The secret key used for securing the application. Loaded from environment variables or defaults to 'default_secret_key'.
        SQLALCHEMY_DATABASE_URI (str): The database URI. Loaded from environment variables or defaults to 'sqlite:///default.db'.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Configuration to disable tracking modifications of objects and emit signals.
        MAIL_SERVER (str): Mail server address. Defaults to 'smtp.gmail.com'.
        MAIL_PORT (int): Mail server port. Defaults to 465.
        MAIL_USE_TLS (bool): Indicates whether to use TLS for the mail server. Defaults to False.
        MAIL_USE_SSL (bool): Indicates whether to use SSL for the mail server. Defaults to True.
        MAIL_USERNAME (str): Username for the mail server. Loaded from environment variables.
        MAIL_PASSWORD (str): Password for the mail server. Loaded from environment variables.
        MAIL_DEFAULT_SENDER (tuple): Default sender email address and name. Loaded from environment variables.
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///default.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('VARRS Support', os.getenv('MAIL_USERNAME'))

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
