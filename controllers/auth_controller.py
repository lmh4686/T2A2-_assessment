from flask import Blueprint, request, abort
from models.employees import Employee, EmployeeSchema
from db import db, jwt, bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from sqlalchemy.exc import IntegrityError
import os


auth = Blueprint('auth', __name__, url_prefix='/auth/')
    
    
class Security:
    office_pw = os.environ.get('OFFICE_PASSWORD')
    
    def authorize():
        emp_id = get_jwt_identity() 
        stmt = db.select(Employee).filter_by(id=emp_id) # Select an employee whose id is equal to jwt's identity
        emp = db.session.scalar(stmt) # execute stmt and return the employee satisfied stmt.
        if not emp or not emp.is_admin:
            abort(401)


@auth.route('register/', methods=['POST'])
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
            name = fields['name'],
            is_admin = False
        )
        
        db.session.add(employee)
        db.session.commit()
        
        token = create_access_token(identity= str(employee.id), expires_delta=timedelta(days=1))
        
        return {"New employee": EmployeeSchema().dump(employee), "Token": token}, 201 # Created
    
    except IntegrityError:
        return {"err": "Existing username."}, 409


@auth.route('login/', methods=['POST'])
def login():
    fields = request.json
    stmt = db.select(Employee).filter_by(username = fields['username'])
    employee = db.session.scalar(stmt)
    if not employee or not bcrypt.check_password_hash(employee.password, fields['password']):
        return {"err": "Wrong username or password"}, 401 #Unauthorized
    
    token = create_access_token(identity=employee.id, expires_delta=timedelta(days=1))

    return {"Logged in employee": EmployeeSchema(exclude=['username']).dump(employee), "Token": token}


@auth.route('<int:id>/fire', methods=['DELETE'])
@jwt_required()
def fire(id):
    authorize()

    stmt = db.select(Employee).filter_by(id=id)
    emp = db.session.scalar(stmt)

    if not emp:
        return {'err': 'Employee not found'}, 404

    db.session.delete(emp)
    db.session.commit()
    return {'Fired employee': EmployeeSchema().dump(emp)}


@auth.route('<int:id>/update', methods=['PUT', 'PATCH'])
@jwt_required()
def update(id):
    authorize()
    fields = EmployeeSchema().load(request.json)
    stmt = db.select(Employee).filter_by(id=id)
    emp = db.session.scalar(stmt)
    
    if not emp:
        return {'err': f'Employee not found with id {id}'}, 404
    
    if not fields:
        return {'err': 'Provide at least one field to update.'}, 400
    
    emp.username = fields.get('username') or emp.username
    emp.password = fields.get('password') or emp.password
    emp.name = fields.get('name') or emp.name
    
    db.session.commit()
    return EmployeeSchema().dump(emp)
    