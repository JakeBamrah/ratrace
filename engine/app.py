import os

import flask
from flask_cors import CORS

from db.database import Session
import blueprints


def create_app(config='dev'):
    app = flask.Flask(__name__, instance_relative_config=True)

    CORS(app)

    if config == 'dev':
        app.config.from_object('config.DevConfig')
    else:
        app.config.from_object('config.ProductionConfig')

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.before_request
    def session_create():
        flask.g.session = Session

    @app.teardown_appcontext
    def shutdown_session(response_or_exc):
        flask.g.session.remove()

    app.register_blueprint(blueprints.orgs)
    app.register_blueprint(blueprints.account)

    return app
