from flask import Flask
from db import db, ma, jwt, bcrypt
import os

def create_app():
    app = Flask(__name__)
    app.config['JSON_SORT_KEYS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['JWT_SECRET_KEY'] = os.environ.get("SECRET_KEY")
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    
    from commands import db_commands
    app.register_blueprint(db_commands)

    from controllers import controllers
    for controller in controllers:
        app.register_blueprint(controller)

    return app
