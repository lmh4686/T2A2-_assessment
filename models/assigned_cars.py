from init import db, ma
from marshmallow.validate import OneOf

VALID_STATUS = ("Ongoing", "Over due", "Sold")


class AssignedCar(db.Model):
    __tablename__ = 'assigned_cars'

    id = db.Column(db.Integer, primary_key=True)
    assigned_date = db.Column(db.Date, nullable=False)
    sale_goal_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(10), nullable=False)
    
    emp_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey("cars.id"), nullable=False)
    
    employee = db.relationship("Employee", back_populates="assigned_cars")
    car = db.relationship("Car", back_populates="assigned_car")
    

class AssignedCarSchema(ma.Schema):
    class Meta:
            ordered = True
            fields = ('id', 'emp_id', 'car_id', 'assigned_date', 'sale_goal_date', 'status')