from flask import Blueprint, request
from controllers.auth_controller import Security
from models.bodies import Body, BodySchema
from init import db
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError
from defs import data_retriever

bodies = Blueprint('bodies', __name__, url_prefix='/bodies/')

@bodies.route('/', methods=['POST'])
@jwt_required()
def create_body():
    Security.authorize()

    fields = BodySchema().load(request.json)
    
    # select the record from the Body that all rows are the same with fields's values except id.
    stmt = db.select(Body).filter_by(
        type=fields['type'],
        size=fields['size'])
    
    duplication = db.session.scalar(stmt)
    
    if duplication:
        return {'err': 'Record already exists'}, 409 
    
    body = Body(type = fields['type'],
                size = fields['size'])
    
    db.session.add(body)
    db.session.commit()


@bodies.route('/')
@jwt_required()
def all_bodies():
    #Select all from Body. query statement & execution & json transformation all in one
    
    # return BodySchema(many=True).dump(db.session.execute(db.select(Body)).scalars())
    bodies = data_retriever(Body)
    return BodySchema(many=True).dump(bodies)

@bodies.route('/<int:id>/')
@jwt_required()
def get_one_body(id):
    Security.authorize()
    # Extract a body that id is equal to the given id in the uri parameter
    # Execution & query statement all in one.
    # body = db.session.execute(db.select(Body).filter_by(id=id)).scalar()
    # if not body:
    #     return {'err': f"Body that has id {id} not found"}, 404
    body = data_retriever(Body, id)
    if not body:
        return {'err': f"Body that has id {id} not found"}, 404
    
    return BodySchema().dump(body)

