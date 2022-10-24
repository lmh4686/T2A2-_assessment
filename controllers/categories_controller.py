from flask import Blueprint, request
from models.categories import Category, CategorySchema
from models.employees import Employee
from db import db
from flask_jwt_extended import jwt_required, get_jwt_identity

categories = Blueprint('categories', __name__, url_prefix='/categories/')

@categories.route("add/", methods=['POST'])
@jwt_required()
def add_category():
    emp_id = get_jwt_identity()
    stmt = db.select(Employee).filter_by(id=emp_id)
    emp = db.session.scalar(stmt)
    
    if not emp:
        return {'err': 'Unauthorized access'}, 401
    
    field = request.json
    category = Category(
        name = field['name']
    )
    
    db.session.add(category)
    db.session.commit()
    
    return {'New category': CategorySchema().dump(category)}