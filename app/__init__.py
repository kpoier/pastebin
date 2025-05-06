from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # config
    app.config.from_object('config.Config')
    app.static_folder = app.config['STATIC_FOLDER']
    app.static_url_path = app.config['STATIC_URL']
    app.secret_key = app.config['SECRET_KEY']

    # database
    app.SQLALCHEMY_DATABASE_URI = app.config['SQLALCHEMY_DATABASE_URI']
    db.init_app(app)

    with app.app_context():
        from app.router import main_bp
        app.register_blueprint(main_bp)
        from app.model import Paste
        db.create_all()

    return app