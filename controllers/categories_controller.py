from flask import Blueprint, request
from controllers.auth_controller import Security
from db import db
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError

categories = Blueprint('categories', __name__, url_prefix='/categories/')

@categories.route("add/", methods=['POST'])
@jwt_required()
def add_category():
    authorize()
    try:
        field = CategorySchema().load(request.json)
        category = Category(name = field['name'])
        db.session.add(category)
        db.session.commit()
        return {'New category': CategorySchema().dump(category)}
    except IntegrityError:
        return {'err': 'Category already exists'}
    
