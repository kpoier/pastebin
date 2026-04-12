import os

class Config:
    SECRET_KEY = 'your_secret_key'
    STATIC_FOLDER = '../static'
    STATIC_URL = '/static'
    TEMPLATE_FOLDER = '../static/html/'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    MAX_CONTENT_LENGTH = 25 * 1024 * 1024
    
    ADMIN_USERNAME = 'admin'
    ADMIN_PASSWORD = 'supersecretpassword'
    ADMIN_URL_PREFIX = '/manage'