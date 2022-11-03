from dataclasses import fields
from sqlite3 import TimeFromTicks
from flask import Blueprint, request
from init import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.stocks import Stock, StockSchema
from models.brands import Brand
from models.employees import Employee
from sqlalchemy.exc import IntegrityError
from controllers.auth_controller import Security
from functions import data_retriever
from models.trims import Trim

stocks = Blueprint('stocks', __name__, url_prefix="/stocks")

@stocks.route('/')
@jwt_required()
def get_all_stocks():
    return StockSchema(many=True).dump(data_retriever(Stock))


@stocks.route('/<int:id>/')
@jwt_required()
def get_one_stock(id):
    stock = data_retriever(Stock, id)
    
    if not stock:
        return {'err': f'Stock that has id {id} not found'}, 404
    return StockSchema().dump(stock)


@stocks.route('/', methods=['POST'])
@jwt_required()
def create_stock():
    fields = StockSchema().load(request.json)
    
    trim = data_retriever(Trim, fields['trim_id'])
    if not trim:
        return {'err': f"Given trim_id {fields['trim_id']} not found in the Trim"}, 404
    
    stock = Stock(
        rego = fields['rego'],
        price = fields['price'],
        driven_km = fields['driven_km'],
        color = fields['color'].capitalize(),
        trim_id = fields['trim_id']
    )
    
    db.session.add(stock)
    
    try:
        db.session.commit()
    except IntegrityError:
        return {'err': 'Same rego already exists.'}, 409
    
    return {'New stock': StockSchema().dump(stock)}, 201
    

@stocks.route('/<int:id>/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_stock(id):
    stock = data_retriever(Stock, id)
    if not stock:
        return {"err": f"Given stock id {id} does not exist"}, 404
    
    fields = StockSchema().load(request.json)
    
    if not fields:
        return {"err": 'At least one field required : rego, price,'
                ' driven_km, color, trim_id'}, 400
    
    temp_rego = fields.get('rego') or stock.rego
    temp_price = fields.get('price') or stock.price
    temp_driven_km = fields.get('driven_km') or stock.driven_km
    temp_color = fields['color'].capitalize() if 'color' in fields else stock.color
    temp_trim_id = fields.get('trim_id') or stock.trim_id
    
    trim = data_retriever(Trim, temp_trim_id)
    if not trim:
        return {'err': f"Given trim_id {temp_trim_id} not found in the Trim."}, 404
    
    # Select a stock that has the same values with the fields except primary key.
    stmt = db.select(Stock).filter_by(rego=temp_rego,
                                      price=temp_price,
                                      driven_km= temp_driven_km,
                                      color=temp_color,
                                      trim_id= temp_trim_id)
    duplication = db.session.scalar(stmt)
    
    if duplication:
        return {'err': 'Record already exists'}, 409
    
    stock.rego = temp_rego
    stock.price = temp_price
    stock.driven_km = temp_driven_km
    stock.color = temp_color
    stock.trim_id = temp_trim_id
      
    try:
        db.session.commit()
    except IntegrityError:
        return {'err': 'Same rego already exists'}, 409
    
    return {'Updated stock': StockSchema().dump(stock)}


@stocks.route('/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete_stock(id):
    Security.authorize('manager')
    stock = data_retriever(Stock, id)
    
    if not stock:
        return {'err': f"Provided stock id {id} not found"}, 404
    
    db.session.delete(stock)
    db.session.commit()
    
    return {"message": f"Stock {id} has been deleted"}
