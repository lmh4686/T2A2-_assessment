from flask import Blueprint, request, abort
from models.employees import Employee, EmployeeSchema
from db import db, jwt, bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from sqlalchemy.exc import IntegrityError
import os


auth = Blueprint('auth', __name__, url_prefix='/auth')
    
    
class Security:
    office_pw = os.environ.get('OFFICE_PASSWORD')
    
    def authorize():
        emp_id = get_jwt_identity() 
        # Select an employee whose id is equal to current jwt's identity
        stmt = db.select(Employee).filter_by(id=emp_id) 
        # execute stmt and return the employee satisfied stmt.
        emp = db.session.scalar(stmt)
        if not emp or not emp.is_admin:
            abort(401)


@auth.route('/employees/')
@jwt_required()
def get_all_employees():
    Security.authorize()
    #Extract all employees/json conversion & execution & query statement all in one.
    return EmployeeSchema(many=True).dump(db.session.execute
                                         (db.select(Employee))
                                         .scalars())
    
@auth.route('/<int:id>/employee/')
@jwt_required()
def get_one_employee(id):
    Security.authorize()
    #Extract one employee whose id is equal to the given id in the uri parameter
    return EmployeeSchema().dump(db.session.execute
                                (db.select(Employee)
                                .filter_by(id=id))
                                .scalar())

@auth.route('/register/', methods=['POST'])
def register():
    if request.json["office_pw"] == Security.office_pw:
        del request.json['office_pw']
    else:
        return {'err': 'Wrong office password'}, 401
    
    fields = EmployeeSchema().load(request.json)
    try:
        employee = Employee(
            username = fields['username'],
            password = bcrypt.generate_password_hash(fields['password']).decode('utf8'),
            f_name= fields['f_name'].capitalize(),
            l_name= fields['l_name'].capitalize(),
            ph = fields['ph'],
            is_admin = False
        )       
        db.session.add(employee)
        db.session.commit()
        
        token = create_access_token(identity=str(employee.id), expires_delta=timedelta(days=15))
        
        return {"New employee": EmployeeSchema().dump(employee), "Token": token}, 201
    
    except IntegrityError:        
        return {"err": "Existing username or phone number."}, 409


@auth.route('/login/', methods=['POST'])
def login():
    fields = request.json
    #Select an employee whose username is equal to username field in request body.
    stmt = db.select(Employee).filter_by(username = fields['username'])
    employee = db.session.scalar(stmt)
    if not employee or not bcrypt.check_password_hash(employee.password, fields['password']):
        return {"err": "Wrong username or password"}, 401 #Unauthorized
    
    token = create_access_token(identity=employee.id, expires_delta=timedelta(days=15))

    return {"Logged in employee": EmployeeSchema(exclude=['username']).dump(employee), "Token": token}


@auth.route('/self/update/', methods=['PUT', 'PATCH'])
@jwt_required()
def self_update():
    fields = EmployeeSchema().load(request.json)
    # Select an employee whose id is equal to current jwt's identity 
    stmt = db.select(Employee).filter_by(id=get_jwt_identity())
    emp = db.session.scalar(stmt)
    
    if not fields:
        return {'err': 'Provide at least one field to update.'}, 400
    
    emp.username = fields.get('username') or emp.username
    emp.password = bcrypt.generate_password_hash(
        fields.get('password')
        ).decode('utf8') or emp.password
    emp.f_name = fields["f_name"].capitalize() if "f_name" in fields else emp.f_name
    emp.l_name = fields["l_name"].capitalize() if "l_name" in fields else emp.l_name
    emp.ph = fields.get('ph') or emp.ph
    
    try:
        db.session.commit()
    except IntegrityError:
        return {"err": "Existing username or phone number."}, 409
    
    return {"Updated employee": EmployeeSchema().dump(emp)}
    
    
@auth.route('<int:id>/discharge/', methods=['DELETE'])
@jwt_required()
def delete_emp(id):
    Security.authorize()
    #Select an employee whose id matches with the given id in the uri parameter
    stmt = db.select(Employee).filter_by(id=id)
    emp = db.session.scalar(stmt)

    if not emp:
        return {'err': f"Employee not found with matching id {id}"}, 404

    db.session.delete(emp)
    db.session.commit()
    return {'Discharged employee': EmployeeSchema().dump(emp)}