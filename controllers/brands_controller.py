from flask import Blueprint, request
from models.brands import Brand, BrandSchema
from controllers.auth_controller import Security
from db import db
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError

brands = Blueprint('brands', __name__, url_prefix='/brands')


@brands.route('/register/', methods=['POST'])
@jwt_required()
def create_brand():
    Security.authorize()
    
    fields = BrandSchema().load(request.json)
    brand = Brand(
        name = fields['name'].capitalize()
    )
    
    db.session.add(brand)
    try:
        db.session.commit()
    except IntegrityError:
        return {'err': 'Same brand name already exists'}, 409
    
    return {'Registered brand': BrandSchema().dump(brand)}, 201


@brands.route('<int:id>/update/', methods=['PUT', 'PATCH'])
@jwt_required()
def update(id):
    Security.authorize()
    fields = BrandSchema().load(request.json)

    if not fields:
        return {'err': "Field 'name' required."}, 400
    #Select brand that has the same id with given id in the uri parameter 
    stmt = db.select(Brand).filter_by(id=id)
    brand = db.session.scalar(stmt)

    brand.name = fields["name"].capitalize()

    try:
        db.session.commit()
    except IntegrityError:
        return {"err": "Brand name already exists."}, 409
    
    return {"Updated brand": BrandSchema().dump(brand)}


@brands.route('/')
@jwt_required()
def get_all_brands():
    Security.authorize()
    #Extract all brands/json conversion & execution & query statement all in one.
    return BrandSchema(many=True).dump(db.session.execute(db.select(Brand)).scalars())
    

@brands.route('/<int:id>/')
@jwt_required()
def get_one_brand(id):
    Security.authorize()
    # Extract a brand that id is equal to the given id in the uri parameter
    # Execution & query statement all in one.
    brand = db.session.execute(db.select(Brand).filter_by(id=id)).scalar()
    if not brand:
        return {'err': f"Brand that has id {id} not found"}, 404
    return BrandSchema().dump(brand)


@brands.route('/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete_one_brand(id):
    Security.authorize('manager')
    # Extract a brand that id is equal to the given id in the uri parameter/
    # Execution & query statement all in one.
    brand = db.session.execute(db.select(Brand).filter_by(id=id)).scalar()
    
    if not brand:
        return {'err': f"Brand that has id {id} not found"}, 404
    
    db.session.delete(brand)
    
    try:
        db.session.commit()
    except IntegrityError:      
        return {'err': f'Can not delete this brand.'
                        ' There are record(s) depending on this brand in the Model'} ,409
    
    return {'message': f'{brand.name} has been removed'}
    

