from db import db, ma
from marshmallow import fields

class Car(db.Model):
    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey("brands.id"), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)
    name = db.Column(db.String(15), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    is_offroad = db.Column(db.Boolean(), default=False)
    year = db.Column(db.Integer, nullable=False)
    km = db.Column(db.Integer, nullable=False)

class CarSchema(ma.Schema):
    class Meta:
        ordered = True # Fields from other tables need to be matched backref
        fields = ('id','category', 'brand', 'employee', 'name', 'price', 'is_offroad', 'year', 'km')
    category = fields.Nested("CategorySchema", only=('name',))
    brand = fields.Nested("BrandSchema", only=('name',))
    employee = fields.Nested("EmployeeSchema", only=('id', 'name', 'is_admin',))
    
    

    
