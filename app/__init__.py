from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.static_folder = app.config['STATIC_FOLDER']
    app.static_url_path = app.config['STATIC_URL']

    return app