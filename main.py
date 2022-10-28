from flask import Flask
from db import db, ma, jwt, bcrypt
import os
from marshmallow.exceptions import ValidationError


def create_app():
    app = Flask(__name__)
    
    @app.errorhandler(KeyError)
    def key_error(e):
        return {"err": f"Missing {str(e)} field"}, 400
    
    @app.errorhandler(400)
    def bad_request(e):
        return {"err": str(e)}, 400
    
    @app.errorhandler(ValidationError)
    def val_error(e):
        return e.messages, 400
    
    @app.errorhandler(401)
    def not_authorized(e):
        return {"err": str(e)}, 401
    
    @app.errorhandler(404)
    def not_found(e):
        return {"err": str(e)}, 404    
    
    @app.errorhandler(405)
    def method_err(e):
        return {"err": str(e)}, 405
    
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
