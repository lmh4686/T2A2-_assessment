from flask import Blueprint, request, abort
from models.employees import Employee, EmployeeSchema
from init import db, bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from sqlalchemy.exc import IntegrityError
from functions import data_retriever
import os


auth = Blueprint('auth', __name__, url_prefix='/auth')
    
    
class Security:
    
    office_pw = os.environ.get('OFFICE_PASSWORD')
    
    def authorize(position='all'):
        emp_id = get_jwt_identity() 
        # Select an employee whose id is equal to current jwt's identity
        stmt = db.select(Employee).filter_by(id=emp_id) 
        # Get one of stmt
        emp = db.session.scalar(stmt)
        
        if not emp:
            abort(401)
        
        if position == 'manager' and not emp.is_admin:
            abort(401, 'Only managers are granted to access')
     
        return emp
            
        
@auth.route('/employees/')
@jwt_required()
def get_all_employees():
    Security.authorize('manager')
    return EmployeeSchema(many=True).dump(data_retriever(Employee))

    
@auth.route('/<int:id>/employee/')
@jwt_required()
def get_one_employee(id):
    Security.authorize('manager')
    emp = data_retriever(Employee, id)
    
    if not emp:
        return {'err': f'No employee found with id {id}'}, 404
    
    return EmployeeSchema().dump(emp)


@auth.route('/register/', methods=['POST'])
def create_employee():
    if request.json["office_pw"] == Security.office_pw:
        del request.json['office_pw']
    else:
        return {'err': 'Wrong office password'}, 401
    
    fields = EmployeeSchema().load(request.json)

    employee = Employee(
        username = fields['username'],
        password = bcrypt.generate_password_hash(fields['password']).decode('utf8'),
        f_name= fields['f_name'].capitalize(),
        l_name= fields['l_name'].capitalize(),
        ph = fields['ph'],
        is_admin = False
    )       
    db.session.add(employee)
    
    try:
        db.session.commit()
    except IntegrityError:        
        return {"err": "Existing username or phone number."}, 409

    token = create_access_token(identity=str(employee.id), expires_delta=timedelta(minutes=15))
    
    return {"New employee": EmployeeSchema().dump(employee), "Token": token}, 201
    
    
@auth.route('/login/', methods=['POST'])
def login():
    fields = request.json
    #Select an employee whose username is equal to username field in request body.
    stmt = db.select(Employee).filter_by(username = fields['username'])
    # get one of stmt
    employee = db.session.scalar(stmt)
    if not employee or not bcrypt.check_password_hash(employee.password, fields['password']):
        return {"err": "Wrong username or password"}, 401 
    
    token = create_access_token(identity=employee.id, expires_delta=timedelta(minutes=15))

    return {"Logged in employee": EmployeeSchema(exclude=['username']).dump(employee), "Token": token}


@auth.route('/self/update/', methods=['PUT', 'PATCH'])
@jwt_required()
def employee_self_update():
    emp = Security.authorize()
    fields = EmployeeSchema().load(request.json)

    if not fields:
        return {'err': 'At least one of the field required:'
                "'username', 'password', 'f_name', 'l_name', 'ph'"}, 400
    
    emp.username = fields.get('username') or emp.username
    emp.password = bcrypt.generate_password_hash(fields['password']).decode('utf8') if 'password' in fields else emp.password
    emp.f_name = fields["f_name"].capitalize() if "f_name" in fields else emp.f_name
    emp.l_name = fields["l_name"].capitalize() if "l_name" in fields else emp.l_name
    emp.ph = fields.get('ph') or emp.ph
    
    try:
        db.session.commit()
    except IntegrityError:
        return {"err": "Existing username or phone number."}, 409
    
    return {"Updated employee": EmployeeSchema().dump(emp)}
    
    
@auth.route('/<int:id>/discharge/', methods=['DELETE'])
@jwt_required()
def delete_employee(id):
    Security.authorize('manager')

    emp = data_retriever(Employee, id)

    if not emp:
        return {'err': f"Employee not found with matching id {id}"}, 404

    db.session.delete(emp)
    db.session.commit()
    return {'Discharged employee': EmployeeSchema().dump(emp)}