import os

class Config:
    SECRET_KEY = 'your_secret_key'
    STATIC_FOLDER = '../static'
    STATIC_URL = '/static'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')