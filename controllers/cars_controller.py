from flask import Blueprint, request
from db import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.cars import Car, CarSchema
from models.brands import Brand
from models.employees import Employee
from sqlalchemy.exc import IntegrityError
from controllers.auth_controller import authorize

cars = Blueprint('cars', __name__, url_prefix="/cars")

@cars.route("/all/")
@jwt_required()
def all_cars():
    stmt = db.select(Car) # Select all cars
    cars = db.session.scalars(stmt) # Execute stmt & return all cars
    return CarSchema(many=True).dump(cars)


@cars.route("/add/", methods=['POST'])
@jwt_required()
def add_car():
    emp_id = get_jwt_identity()
    stmt = db.select(Employee).filter_by(id=emp_id)
    emp = db.session.scalar(stmt)
    
    if not emp:
        return {'err': 'Unauthorized access'}, 401
    

    field = request.json
    car = Car(
        category_id = db.select(Category.id).filter(Category.name == field['category']),
        brand_id = db.select(Brand.id).filter(Brand.name == field['brand']),
        employee_id = db.select(Employee.id).filter(Employee.name == field['employee']),
        name = field['name'],
        price = field['price'],
        is_offroad = field['is_offroad'],
        year = field['year'],
        km = field['km']
    )
    
    db.session.add(car)
    db.session.commit()
    
    return {'New car': CarSchema().dump(car)}
    

@cars.route("/price_range/")
def price_range():
    field = request.json
    stmt = db.select(Car).filter(Car.price>int(field['min']), Car.price<int(field['max']))
    cars = db.session.scalars(stmt)
    print(cars)
    return CarSchema(many=True).dump(cars)
    

@cars.route("/filter")
def filter_cars():
    field = request.json 
    if "brand" not in field.keys():
        stmt = db.select(Car).filter(Car.year >= field["min_year"], Car.year <= field["max_year"], Car.km >= field["min_km"], Car.km <= field["max_km"], Car.price >= field["min_price"], Car.price <= field["max_price"])
    else:
        brand = db.select(Brand.id).filter_by(name = field["brand"])
        stmt = db.select(Car).filter(Car.brand_id == brand, Car.year >= field["min_year"], Car.year <= field["max_year"], Car.km >= field["min_km"], Car.km <= field["max_km"], Car.price >= field["min_price"], Car.price <= field["max_price"])
    cars = db.session.scalars(stmt)
    return CarSchema(many=True).dump(cars)

