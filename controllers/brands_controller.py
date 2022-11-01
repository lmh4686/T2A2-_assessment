from flask import Blueprint, request
from models.brands import Brand, BrandSchema
from controllers.auth_controller import Security
from init import db
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError
from functions import data_retriever

brands = Blueprint('brands', __name__, url_prefix='/brands')


@brands.route('/', methods=['POST'])
@jwt_required()
def create_brand():
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


@brands.route('/<int:id>/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_brand(id):
    fields = BrandSchema().load(request.json)

    brand = data_retriever(Brand, id)
    
    if not brand :
        return {'err': f"Brand record with id '{id}' not found"}, 404
    
    brand.name = fields["name"].capitalize()

    try:
        db.session.commit()
    except IntegrityError:
        return {"err": "Brand name already exists."}, 409
    
    return {"Updated brand": BrandSchema().dump(brand)}


@brands.route('/')
@jwt_required()
def get_all_brands():
    return BrandSchema(many=True).dump(data_retriever(Brand))
    

@brands.route('/<int:id>/')
@jwt_required()
def get_one_brand(id):
    brand = data_retriever(Brand, id)
    
    if not brand :
        return {'err': f"Brand that has id {id} not found"}, 404
    
    return BrandSchema().dump(brand)


@brands.route('/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete_brand(id):
    Security.authorize('manager')

    brand = data_retriever(Brand, id)
    
    if not brand :
        return {'err': f"Brand that has id {id} not found"}, 404
    
    db.session.delete(brand)
    
    try:
        db.session.commit()
    except IntegrityError:      
        return {'err': f'Can not delete this brand.'
                        ' There are record(s) depending on this brand'} ,409
    
    return {'message': f'{brand.name} has been removed'}
    

