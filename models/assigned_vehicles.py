from init import db, ma
from marshmallow.validate import OneOf, Range
from datetime import timedelta, date
from marshmallow import fields


fk_validator = ma.Integer(validate=Range(min=1))
VALID_STATUS = ("Ongoing", "Overdue", "Sold")


class AssignedVehicle(db.Model):
    __tablename__ = 'assigned_vehicles'

    id = db.Column(db.Integer, primary_key=True)
    assigned_date = db.Column(db.Date, nullable=False)
    sale_goal_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(8), nullable=False, default='Ongoing')
    
    emp_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey("stocks.id"), nullable=False, unique=True)
    employee = db.relationship("Employee", back_populates="assigned_vehicles")
    stock = db.relationship("Stock", back_populates="assigned_vehicle")
    

class AssignedVehicleSchema(ma.Schema):
    stock = fields.Nested('StockSchema', only=['rego', 'price', 'color', 'trim'])
    employee = fields.Nested('EmployeeSchema', only=['f_name', 'l_name', 'ph'])
    class Meta:
        ordered = True
        fields = ('id', 'assigned_date', 'sale_goal_date', 'status', 'emp_id', 'employee', 'stock_id', 'stock')
        
    emp_id = fk_validator
    stock_id = fk_validator
    sale_goal_date = ma.Date(validate=Range(min= date.today() + timedelta(weeks=3),
                                            max= date.today() + timedelta(weeks=15)))
    status = ma.String(load_default='Ongoing', validate=OneOf(VALID_STATUS))
    