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


assigned_vehicles = Blueprint("assigned_vehicles", 
                              __name__, 
                              url_prefix="/assignments")


def authorize_and_retrieve(AV, id):
    Security.authorize('manager')
    av = data_retriever(AV, id)
    
    if not av:
        return abort(404, f'Assigned vehicle that has id {id} not found')
    
    return av


def av_order_by_status():
    # Align all AV records by status's alphabetic order.
    # Ongoing - Overdue - Sold order.
    stmt = db.select(AV).order_by(AV.status)
    # Get all of stmt
    avs = db.session.scalars(stmt)
    return avs


@assigned_vehicles.route('/')
@jwt_required()
def get_all_av():
    Security.authorize('manager')
    avs = av_order_by_status()
    return AVS(many=True).dump(avs)


@assigned_vehicles.route('/<status>/')
@jwt_required()
def get_avs_by_status(status):
    Security.authorize('manager')
    # Select all AV records that status = uri parameter. 
    stmt = db.select(AV).filter_by(status=status)
    # Get one of stmt
    # Not used scalars() because it always return something
    # even when there's no value.
    # which is not suit for the next if statement.
    avs = db.session.scalar(stmt)
    if not avs:
        # Select all status' values in the AV records.
        stmt_status = db.select(AV.status)
        # Get one of stmt_status
        one_status = db.session.scalar(stmt_status)
        
        if not one_status:
            return {'Message': 'There is no assigned_vehicle record at all'}, 404
        
        status_set = set()
        # Get all of stmt_status
        statuses = db.session.scalars(stmt_status)
        
        for i in statuses:
            status_set.add(i)
            
        return {'err': f'No status {status} found.'
                       f' Available statuses to apply: {status_set}'}, 404
    # Get all of stmt
    avs = db.session.scalars(stmt)    
    return AVS(many=True).dump(avs)


@assigned_vehicles.route('/my/')
@jwt_required()
def get_my_av():
    emp = Security.authorize()
    # Select all AV records that emp_id is equal to 
    # currently logged in employee's id
    stmt = db.select(AV).filter_by(emp_id = emp.id)
    # Use scalar() to check if it's none or not
    av = db.session.scalar(stmt)
    
    if not av:
        return {'message': "You don't have any assigned vehicle."}, 404
    # scalars() to extract all records
    av = db.session.scalars(stmt)
    return AVS(many=True).dump(av)


@assigned_vehicles.route('/<int:id>/')
@jwt_required()
def get_av_by_id(id):
    av = authorize_and_retrieve(AV, id)
    return AVS().dump(av)


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


@assigned_vehicles.route('/<int:id>/', methods=['PUT', 'PATCH'])
@jwt_required()
def manager_update_av(id):
    av = authorize_and_retrieve(AV, id)
    fields = AVS().load(request.json)
    temp_sale_goal_date = fields.get("sale_goal_date")or av.sale_goal_date
    temp_status = fields.get("status") or av.status
    temp_emp_id = fields.get("emp_id") or av.emp_id
    temp_stock_id = fields.get("stock_id") or av.stock_id
    
    emp = data_retriever(Employee, temp_emp_id)
    stock = data_retriever(Stock, temp_stock_id)
    
    if not emp:
        return {'err': f'Employee id {temp_emp_id} not found'}, 404
    if not stock:
        return {'err': f'Stock id {temp_stock_id} not found'}, 404
    
    av.assigned_date = date.today() if av.emp_id != temp_emp_id else av.assigned_date
    av.sale_goal_date = temp_sale_goal_date
    av.status = temp_status
    av.emp_id = temp_emp_id
    av.stock_id = temp_stock_id
    
    try:
        db.session.commit()
    except IntegrityError:
        return {'err': f"The stock id {fields['stock_id']} already assigned."}, 409
    
    return {'Updated assignment': AVS().dump(av)}


@assigned_vehicles.route('/<int:id>/status/', methods=['PATCH'])
@jwt_required()
def update_av_status(id):
    emp = Security.authorize()
    av = data_retriever(AV, id)
    
    if not av:
        return {'err': f"Assigned vehicle id {id} not found"}, 404
    
    if av.emp_id != emp.id and not emp.is_admin:
        # Select all AssignedVehicle's id that 
        # emp_id is equal to currently logged in employee id. 
        stmt = db.select(AV.id).filter_by(emp_id = emp.id)
        # Extract one of stmt
        emp_av_id = db.session.scalar(stmt)
        
        if emp_av_id:
            available_av_id = []
            # Extract all stmt
            emp_av_id = db.session.scalars(stmt)
            for i in emp_av_id:
                available_av_id.append(i)     
        else :
            return {'err': f"Only allowed to update vehicles assigned to you."
                            " And you don't have any assigned vehicle."}, 401
                 
        return {'err': f"Only allowed to update vehicles assigned to you."
                       f' This id(s) of vehicle assigned to you: ' 
                       f'{available_av_id}'}, 401
        
    # Not calling AssignedVehicleSchema because of status default loading.    
    field = request.json
    
    if field['status'] != 'Sold' :
        # Other options will be handled in the next route
        return {'err': "Only can change it to 'Sold'."}, 400
    
    av.status = field['status']
    db.session.commit()
    
    return {'Updated assignment': AVS().dump(av)}


@assigned_vehicles.route('/statuses/', methods=['PATCH'])
@jwt_required()
def update_av_statuses():
    # Select all object that its status is 'Ongoing' and 
    # sale_goal_date is expired.
    stmt = db.select(AV).filter(AV.status == 'Ongoing',
                                AV.sale_goal_date < date.today())
    #Get one of stmt
    avs = db.session.scalar(stmt)
    
    if not avs:
        return {'message': 'Everything is up to date.'}, 404
    # Get all of stmt
    avs = db.session.scalars(stmt)

    for av in avs:
        av.status = 'Overdue'

    db.session.commit()
    
    avs = av_order_by_status()
    return {'Updated complete': AVS(many=True).dump(avs)}


@assigned_vehicles.route('/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete_av(id):
    av = authorize_and_retrieve(AV, id)
    db.session.delete(av)
    db.session.commit()
    return {'message': f"Assigned vehicle with id {id} has been deleted"}
    
        
        