from flask import Blueprint, request
from models.employees import Employee, EmployeeSchema
from db import db, jwt, bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta


auth = Blueprint('auth', __name__, url_prefix='/auth/')
    

@auth.route('register/', methods=['POST'])
def register():
    fields = request.json
    employee = Employee(
        username = fields['username'],
        password = bcrypt.generate_password_hash(fields['password']).decode('utf8'),
        name = fields['name'],
        is_admin = False
    )

    validate = db.select(Employee).filter_by(username=fields['username'])
    is_employee = db.session.scalar(validate)
    
    if is_employee:
        return {'err': 'Try another username'}, 400 # Bad request
    
    db.session.add(employee)
    db.session.commit()
    
    token = create_access_token(identity= str(employee.id), expires_delta=timedelta(days=1))


    return {"New employee": EmployeeSchema().dump(employee), "Token": token}, 201 # Created


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
    emp_id = get_jwt_identity()
    print(emp_id)
    stmt = db.select(Employee).filter_by(id=emp_id)
    emp = db.session.scalar(stmt)
    if not emp:
        return {'err': 'No employee found'}, 400
    if not emp.is_admin:
        return {'err': 'Unauthorized employee'}, 401

    stmt = db.select(Employee).filter_by(id=id)
    emp = db.session.scalar(stmt)

    if not emp:
        return {'err': 'Employee not found'}, 400

    db.session.delete(emp)
    db.session.commit()
    return {'Fired employee': EmployeeSchema().dump(emp)}
    

