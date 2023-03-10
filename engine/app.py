import os
import logging

import flask
from flask_cors import CORS
from flask_session import Session as FlaskSession

import blueprints
from db.database import Session as DBSession


FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('server')


def create_app(config='dev'):
    app = flask.Flask(__name__, instance_relative_config=True)

    if config == 'dev':
        app.config.from_object('config.DevConfig')
    else:
        app.config.from_object('config.ProductionConfig')

    app.secret_key = app.config['SECRET_KEY']

    # setup flask plugins
    CORS(app, supports_credentials=True)
    FlaskSession(app)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.before_request
    def session_create():
        flask.g.session = DBSession

        if 'db_commit' not in flask.g:
            flask.g.db_commit = commit

    @app.teardown_appcontext
    def shutdown_session(response_or_exc):
        flask.g.session.remove()

    def commit(session, objs):
        """
        Simple decorator that wraps sqlalchemy object creation in a session context
        and attempts a commit.
        """
        try:
            session.add_all(objs)
            session.commit()
        except Exception as e:
            logger.error(e)
            session.rollback()
            return False

        return True

    app.register_blueprint(blueprints.account)
    app.register_blueprint(blueprints.auth)
    app.register_blueprint(blueprints.orgs)

    return app
