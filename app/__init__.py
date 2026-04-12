from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # config
    app.config.from_object('config.Config')
    app.template_folder = app.config['TEMPLATE_FOLDER']
    app.static_folder = app.config['STATIC_FOLDER']
    app.static_url_path = app.config['STATIC_URL']
    app.secret_key = app.config['SECRET_KEY']

    # database
    app.SQLALCHEMY_DATABASE_URI = app.config['SQLALCHEMY_DATABASE_URI']
    db.init_app(app)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    with app.app_context():
        from app.router import main_bp
        app.register_blueprint(main_bp)
        
        from app.admin import admin_bp
        app.register_blueprint(admin_bp, url_prefix=app.config['ADMIN_URL_PREFIX'])
        
        from app.model import Paste
        db.create_all()

    return app