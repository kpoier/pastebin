from flask import Flask

def create_app():
    app = Flask(__name__)

    # config
    app.config.from_object('config.Config')
    app.static_folder = app.config['STATIC_FOLDER']
    app.static_url_path = app.config['STATIC_URL']

    # register blueprints
    with app.app_context():
        from app.router import main_bp
        app.register_blueprint(main_bp)

    return app