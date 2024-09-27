from dotenv import load_dotenv
from flask import Flask

from .config import load_config
from .controllers.statistics_controller import stats_blueprint
from .controllers.interactions_controller import interactions_blueprint
from .controllers.products_controller import products_blueprint
from .db import db


# Load env vars from .env, for dev environment to work the same as prod.
# In prod, this line loads nothing as we don't deploy a .env file.
load_dotenv()


def create_app(testing=False):
    app = Flask(__name__)
    app.register_blueprint(stats_blueprint)
    app.register_blueprint(interactions_blueprint)
    app.register_blueprint(products_blueprint)

    conf = load_config(testing)
    app.config.from_object(conf)

    # Initialize the SQLAlchemy extension with the Flask app
    db.init_app(app)

    # Reflect the existing tables from the database
    with app.app_context():
        metadata = db.metadata
        metadata.reflect(bind=db.engine)

    return app
