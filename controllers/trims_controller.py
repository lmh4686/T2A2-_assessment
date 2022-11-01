from flask import Blueprint, request
from controllers.auth_controller import Security
from models.trims import Trim, TrimSchema
from init import db
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError
from functions import data_retriever

trims = Blueprint('trims', __name__, url_prefix='/trims/')


def duplication_checker(fields):
    # select the record from the trim that all rows are the same with fields's values except primary key.
    stmt = db.select(Trim).filter_by(
        name=fields['name'].capitalize(),
        body_type=fields['body_type'],
        model_id=fields['model_id'],
        )
    
    duplication = db.session.scalar(stmt)
    return duplication


@trims.route('/', methods=['POST'])
@jwt_required()
def create_trim():
    fields = TrimSchema().load(request.json)
    
    duplication = duplication_checker(fields)
    
    if duplication:
        return {'err': 'Record already exists'}, 409 
    
    trim = Trim(name = fields['name'].capitalize(),
                body_type = fields['body_type'],
                model_id = fields['model_id'])
    
    db.session.add(trim)
    db.session.commit()
    
    return {"Created trim": TrimSchema().dump(trim)}


@trims.route('/')
@jwt_required()
def all_trims():
    return TrimSchema(many=True).dump(data_retriever(Trim))


@trims.route('/<int:id>/')
@jwt_required()
def get_one_trim(id):
    trim = data_retriever(Trim, id)
    
    if not trim:
        return {'err': f"Trim that has id {id} not found"}, 404
    
    return TrimSchema().dump(trim)


@trims.route('/<int:id>/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_trim(id):
    fields = TrimSchema().load(request.json)

    if not fields:
        return {'err': "Field 'name' or 'body_type' or 'model_id' required."}, 400

    trim = data_retriever(trim, id)
    
    if not trim:
        return {'err': f"Trim name with id '{id}' not found"}, 404
    
    trim.name = fields.get("name") or trim.name
    trim.body_type = fields.get("body_type") or trim.body_type
    
    try:
        db.session.commit()
    except IntegrityError:
        return {"err": "trim name already exists."}, 409
    
    return {"Updated trim": TrimSchema().dump(trim)}


@trims.route('/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete_trim(id):
    Security.authorize('manager')

    trim = data_retriever(Trim, id)
    
    if not trim :
        return {'err': f"Trim that has id {id} not found"}, 404
    
    db.session.delete(trim)
    
    try:
        db.session.commit()
    except IntegrityError:      
        return {'err': f'Can not delete this trim.'
                        ' There are record(s) depending on this trim'} ,409
    
    return {'message': f'{trim.name} has been removed'}