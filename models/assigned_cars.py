from db import db, ma

class AssignedCar(db.Model):
    __tablename__ = 'assigned_cars'

    id = db.Column(db.Integer, primary_key=True)
    sale_due_date = db.Column(db.Date)
    
    emp_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey("cars.id"), nullable=False)
    
    employee = db.relationship("Employee", back_populates="assigned_cars")
    car = db.relationship("Car", back_populates="assigned_car")
    

class AssignedCarSchema(ma.Schema):
    class Meta:
            ordered = True
            fields = ('id', 'emp_id', 'car_id', 'sale_due_date')