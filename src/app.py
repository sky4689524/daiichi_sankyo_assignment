from dotenv import load_dotenv
from flask import Flask

from .config import load_config
from .controllers.statistics_controller import stats_blueprint
from .controllers.interactions_controller import interactions_blueprint
from .controllers.products_controller import products_blueprint
from .controllers.access_controller import access_blueprint

# Load env vars from .env, for dev environment to work the same as prod.
# In prod, this line loads nothing as we don't deploy a .env file.
load_dotenv()


def create_app(testing=False):
    app = Flask(__name__)
    app.register_blueprint(stats_blueprint)
    app.register_blueprint(interactions_blueprint)
    app.register_blueprint(products_blueprint)
    app.register_blueprint(access_blueprint)

    conf = load_config(testing)
    app.config.from_object(conf)

    return app
