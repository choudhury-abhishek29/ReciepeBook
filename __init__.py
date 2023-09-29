from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


db = SQLAlchemy()
ma = Marshmallow()


def create_app():
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'recipes.db')
    app.config['SECRET_KEY'] = 'secret-key'

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    db.init_app(app)
    app.app_context().push()

    ma.init_app(app)

    with app.app_context():
        db.create_all()

    return app
