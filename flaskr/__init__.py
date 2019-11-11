import os

from flask import Flask
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity 


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)        

    app.config['JWT_SECRET_KEY'] = 'apple'  # Change this!
    jwt = JWTManager(app)

    from . import index
    app.register_blueprint(index.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app