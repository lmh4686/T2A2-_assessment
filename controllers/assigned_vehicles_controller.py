from models.assigned_vehicles import AssignedVehicle as AV,\
                                     AssignedVehicleSchema as AVS
from init import db
from flask_jwt_extended import jwt_required
from flask import Blueprint, abort, request
from controllers.auth_controller import Security
from functions import data_retriever
from models.employees import Employee
from models.stocks import Stock
from datetime import date
from sqlalchemy.exc import IntegrityError
from datetime import datetime


def authorize_and_retrieve(AV, id):
    Security.authorize('manager')
    av = data_retriever(AV, id)
    
    if not av:
        return abort(404, f'Assigned vehicle with id {id} not found')
    
    return av


assigned_vehicles = Blueprint("assigned_vehicles", 
                              __name__, 
                              url_prefix="/assignments")

@assigned_vehicles.route('/')
@jwt_required()
def get_all_assigned_vehicles():
    Security.authorize('manager')
    return AVS(many=True).dump(data_retriever(AV))


@assigned_vehicles.route('/<int:id>/')
@jwt_required()
def get_one_assigned_vehicles(id):
    av = authorize_and_retrieve(AV, id)
    return AVS().dump(av)


@assigned_vehicles.route('/<int:id>/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_assigned_vehicle(id):
    av = authorize_and_retrieve(AV, id)
    fields = AVS().load(request.json)
    datetime.strptime('15 Jan 2023', '%d %b %Y')
    temp_sale_goal_date = fields.get("sale_goal_date")or av.sale_goal_date
    temp_status = fields.get("status") or av.status
    temp_emp_id = fields.get("emp_id") or av.emp_id
    temp_stock_id = fields.get("stock_id") or av.stock_id
    
    emp = data_retriever(Employee, temp_emp_id)
    stock = data_retriever(Stock, temp_stock_id)
    
    if not emp:
        return {'err': f'Employee with id {temp_emp_id} not found'}, 404
    if not stock:
        return {'err': f'Stock with id {temp_stock_id} not found'}, 404
    
    av.assigned_date = date.today() if av.emp_id != temp_emp_id else av.assigned_date
    av.sale_goal_date = temp_sale_goal_date
    av.status = temp_status
    av.emp_id = temp_emp_id
    av.stock_id = temp_stock_id
    
    try:
        db.session.commit()
    except IntegrityError:
        return {'err': f"The stock id {fields['stock_id']} had been already assigned."}, 409
    
    return {'Updated assignment': AVS().dump(av)}


@assigned_vehicles.route('/', methods=['POST'])
@jwt_required()
def assign_vehicle():
    Security.authorize('manager')
    
    fields = AVS().load(request.json)
    
    emp = data_retriever(Employee, fields['emp_id'])
    
    if not emp:
        return {'err': f"Given emp_id {fields['emp_id']} not found in the Employee."}, 404
    
    av = AV(
        assigned_date = date.today(),
        sale_goal_date = fields['sale_goal_date'],
        status = fields['status'],
        emp_id = fields['emp_id'],
        stock_id = fields['stock_id']
    )
    db.session.add(av)
    
    try:
        db.session.commit()
    except IntegrityError:
        return {'err': f"Stock that has id {fields['stock_id']} already assigned."}, 409
    
    return {'New assigned vehicle': AVS().dump(av)}, 201


@assigned_vehicles.route('/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete_assigned_vehicle(id):
    av = authorize_and_retrieve(AV, id)
    db.session.delete(av)
    db.session.commit()
    
    
    
    