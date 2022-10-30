from flask import Blueprint, request
from models.models import Model, ModelSchema
from controllers.auth_controller import Security
from init import db
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError

models = Blueprint('models', __name__, url_prefix='/models')


@models.route('/register/', methods=['POST'])
@jwt_required()
def create_model():
    Security.authorize()
    
    fields = ModelSchema().load(request.json)
    model = Model(
        name = fields['name'].capitalize()
    )
    
    db.session.add(model)
    try:
        db.session.commit()
    except IntegrityError:
        return {'err': 'Same model name already exists'}, 409
    
    return {'Registered model': ModelSchema().dump(model)}, 201


@models.route('<int:id>/update/', methods=['PUT', 'PATCH'])
@jwt_required()
def update(id):
    Security.authorize()
    fields = ModelSchema().load(request.json)

    if not fields:
        return {'err': "Field 'name' required."}, 400
    #Select model that has the same id with given id in the uri parameter 
    stmt = db.select(Model).filter_by(id=id)
    model = db.session.scalar(stmt)

    model.name = fields["name"].capitalize()

    try:
        db.session.commit()
    except IntegrityError:
        return {"err": "Model name already exists."}, 409
    
    return {"Updated model": ModelSchema().dump(model)}


@models.route('/')
@jwt_required()
def get_all_models():
    Security.authorize()
    #Extract all models/json conversion & execution & query statement all in one.
    return ModelSchema(many=True).dump(db.session.execute(db.select(Model)).scalars())
    

@models.route('/<int:id>/')
@jwt_required()
def get_one_model(id):
    Security.authorize()
    # Extract a model that id is equal to the given id in the uri parameter
    # Execution & query statement all in one.
    model = db.session.execute(db.select(Model).filter_by(id=id)).scalar()
    if not model:
        return {'err': f"Model that has id {id} not found"}, 404
    return ModelSchema().dump(model)


@models.route('/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete_one_model(id):
    Security.authorize('manager')
    # Extract a model that id is equal to the given id in the uri parameter/
    # Execution & query statement all in one.
    model = db.session.execute(db.select(Model).filter_by(id=id)).scalar()
    
    if not model:
        return {'err': f"Model that has id {id} not found"}, 404
    
    db.session.delete(model)
    
    try:
        db.session.commit()
    except IntegrityError:      
        return {'err': f'Can not delete this model.'
                        ' There are record(s) depending on this model in the Model'} ,409
    
    return {'message': f'{model.name} has been removed'}
    

