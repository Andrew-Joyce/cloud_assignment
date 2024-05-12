from flask import Flask
from Program.config import DevelopmentConfig

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from Program.routes import main_bp
    app.register_blueprint(main_bp)

    return app


