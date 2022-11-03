from init import db, ma
from marshmallow.validate import OneOf, Range
from datetime import timedelta, date


fk_validator = ma.Integer(validate=Range(min=1))
VALID_STATUS = ("Ongoing", "Over due", "Sold")


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
    class Meta:
        ordered = True
        fields = ('id', 'emp_id', 'stock_id', 'assigned_date', 'sale_goal_date', 'status')
        
    emp_id = fk_validator
    stock_id = fk_validator
    sale_goal_date = ma.Date(validate=Range(min= date.today() + timedelta(weeks=3)))
    status = ma.String(load_default='Ongoing', validate=OneOf(VALID_STATUS))