from enum import unique
from db import db, ma
from marshmallow import fields

VALID_BRANDS = ()

class Car(db.Model):
    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    rego = db.Column(db.String(10), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    km = db.Column(db.Integer, nullable=False)
    
    model_id = db.Column(db.Integer, db.ForeignKey("models.id"), nullable=False)
    
    assigned_car = db.relationship("AssignedCar",  back_populates='car')
    
    

class CarSchema(ma.Schema):
    class Meta:
        ordered = True # Fields from other tables need to be matched backref
        fields = ('id', 'rego', 'model_id', 'price', 'km')
    # category = fields.Nested("CategorySchema", only=('name',))
    # brand = fields.Nested("BrandSchema", only=('name',))
    # employee = fields.Nested("EmployeeSchema", only=('id', 'name', 'is_admin',))
    
    

    
