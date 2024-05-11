from flask import Flask
from Program.config import DevelopmentConfig

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register Blueprints inside the function to avoid circular imports
    from Program.routes import main_bp
    app.register_blueprint(main_bp)

    return app


