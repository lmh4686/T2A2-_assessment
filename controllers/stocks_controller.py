from flask import Blueprint, request
from init import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.stocks import Stock, StockSchema
from models.brands import Brand
from models.employees import Employee
from sqlalchemy.exc import IntegrityError
from controllers.auth_controller import Security

stocks = Blueprint('stocks', __name__, url_prefix="/stocks")

@stocks.route("/all/")
@jwt_required()
def all_cars():
    stmt = db.select(Stock) # Select all stocks
    stocks = db.session.scalars(stmt) # Execute stmt & return all stocks
    return StockSchema(many=True).dump(stocks)


@stocks.route("/add/", methods=['POST'])
@jwt_required()
def add_car():
    emp_id = get_jwt_identity()
    stmt = db.select(Employee).filter_by(id=emp_id)
    emp = db.session.scalar(stmt)
    
    if not emp:
        return {'err': 'Unauthorized access'}, 401
    

    field = request.json
    car = Stock(
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
    
    return {'New car': StockSchema().dump(car)}
    

@stocks.route("/price_range/")
def price_range():
    field = request.json
    stmt = db.select(Stock).filter(Stock.price>int(field['min']), Stock.price<int(field['max']))
    stocks = db.session.scalars(stmt)
    print(stocks)
    return StockSchema(many=True).dump(stocks)
    

@stocks.route("/filter")
def filter_cars():
    field = request.json 
    if "brand" not in field.keys():
        stmt = db.select(Stock).filter(Stock.year >= field["min_year"], Stock.year <= field["max_year"], Stock.km >= field["min_km"], Stock.km <= field["max_km"], Stock.price >= field["min_price"], Stock.price <= field["max_price"])
    else:
        brand = db.select(Brand.id).filter_by(name = field["brand"])
        stmt = db.select(Stock).filter(Stock.brand_id == brand, Stock.year >= field["min_year"], Stock.year <= field["max_year"], Stock.km >= field["min_km"], Stock.km <= field["max_km"], Stock.price >= field["min_price"], Stock.price <= field["max_price"])
    stocks = db.session.scalars(stmt)
    return StockSchema(many=True).dump(stocks)

