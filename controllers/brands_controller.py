from flask import Blueprint, request
from models.brands import Brand, BrandSchema
from models.employees import Employee
from db import db
from flask_jwt_extended import jwt_required, get_jwt_identity

brands = Blueprint('brands', __name__, url_prefix='/brands/')

@brands.route("add/", methods=['POST'])
@jwt_required()
def add_brand():
    emp_id = get_jwt_identity()
    stmt = db.select(Employee).filter_by(id=emp_id)
    emp = db.session.scalar(stmt)
    
    if not emp:
        return {'err': 'Unauthorized access'}, 401
    
    field = request.json
    brand = Brand(
        name = field['name'],
        country = field['country']
    )
    
    db.session.add(brand)
    db.session.commit()
    
    return {'New brand': BrandSchema().dump(brand)}