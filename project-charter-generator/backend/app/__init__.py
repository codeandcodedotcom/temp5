from flask import Flask
from app.api import test, generation, health
from app.config import Config
from app.utils.logger import get_logger
from flask_cors import CORS

logger = get_logger(__name__)


def create_app():
    """
    Registers blueprints and initializes extensions.
    """
    app = Flask(__name__)
    # CORS(app, origins=["http://localhost:3000"])
    CORS(app)
    app.config["SECRET_KEY"] = Config.SECRET_KEY

    # Register blueprints
    app.register_blueprint(test.bp, url_prefix="/api/test")
    logger.info("Blueprint 'test' registered at /api/test")
    app.register_blueprint(generation.bp, url_prefix="/api/generation")
    logger.info("Blueprint 'generation' registered at /api/generation")
    app.register_blueprint(health.bp, url_prefix="/api")
    logger.info("Blueprint 'health' registered at /api/health")

    return app
