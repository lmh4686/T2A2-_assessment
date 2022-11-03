from flask import Blueprint, request
from controllers.trims_controller import duplication_checker
from models.models import Model, ModelSchema
from controllers.auth_controller import Security
from init import db
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError
from functions import data_retriever
from models.brands import Brand

models = Blueprint('models', __name__, url_prefix='/models')


def duplicate_checker(fields):
    # select the record from the Model that all rows are the same with fields's values except primary key.
    stmt = db.select(Model).filter_by(
        name=fields['name'].capitalize(),
        year=fields['year'],
        brand_id=fields['brand_id']
    )
    
    duplication = db.session.scalar(stmt)
    return duplication


@models.route('/', methods=['POST'])
@jwt_required()
def create_model():
    fields = ModelSchema().load(request.json)
    
    brand = data_retriever(Brand, fields["brand_id"])
    duplication = duplicate_checker(fields)
    
    if not brand:
        return {'err': 'The brand_id not found in the Brand'}, 404
    
    if duplication:
        return {'err': 'The record already exists'}, 409
    
    model = Model(
        brand_id = fields['brand_id'],
        name = fields['name'].capitalize(),
        year = fields['year']
    )
    
    db.session.add(model)
    db.session.commit()

    return {'Registered model': ModelSchema().dump(model)}, 201


@models.route('/<int:id>/', methods=['PUT', 'PATCH'])
@jwt_required()
def update(id):
    fields = ModelSchema().load(request.json)
    model = data_retriever(Model, id)
    
    if not fields:
        return {'err': "At least one of field required: 'name', 'brand_id', 'year'"}, 400
    
    if not model:
        return {'err': f'The model id {id} not found in the Model'}, 404
    
    temp_name=fields["name"].capitalize() if "name" in fields else model.name, 
    temp_year=fields.get("year") or model.year, 
    temp_brand_id=fields.get("brand_id") or model.brand_id
    
    # Select a model that has the same values with the fields except primary key.
    stmt = db.select(Model).filter_by(
                                      name= temp_name, 
                                      year= temp_year, 
                                      brand_id= temp_brand_id)
    duplication = db.session.scalar(stmt)

    if duplication:
        return {'err': 'The record already exists'}, 409

    model.name = temp_name
    model.year = temp_year
    model.brand_id = temp_brand_id
    
    try:
        db.session.commit()
    except IntegrityError:
        return {"err": f"Provided brand_id {fields['brand_id']} does not exist"}, 404
    
    return {"Updated model": ModelSchema().dump(model)}


@models.route('/')
@jwt_required()
def get_all_models():
    return ModelSchema(many=True).dump(data_retriever(Model))
    

@models.route('/<int:id>/')
@jwt_required()
def get_one_model(id):
    model = data_retriever(Model, id)
    if not model:
        return {'err': f"Model that has id {id} not found"}, 404
    return ModelSchema().dump(model)


@models.route('/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete_one_model(id):
    Security.authorize('manager')
    model = data_retriever(Model, id)
    
    if not model:
        return {'err': f"Model that has id {id} not found"}, 404
    
    db.session.delete(model)
    
    try:
        db.session.commit()
    except IntegrityError:      
        return {'err': f'Can not delete this model.'
                        ' Record(s) exist depending on this model.'} ,409
    
    return {'message': f'{model.name} has been removed'}
    

