from init import db, ma
from marshmallow import fields


class Stock(db.Model):
    __tablename__ = 'stocks'

    id = db.Column(db.Integer, primary_key=True)
    rego = db.Column(db.String(10), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    driven_km = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String, nullable=False)
    
    trim_id = db.Column(db.Integer, db.ForeignKey("trims.id"), nullable=False)
    
    assigned_vehicle = db.relationship("AssignedVehicle",  back_populates='stock', cascade="all, delete")
    trim = db.relationship("Trim",  back_populates='stocks')
    
    

class StockSchema(ma.Schema):
    class Meta:
        ordered = True 
        fields = ('id', 'rego', 'trim_id', 'price', 'driven_km', 'color')
    # category = fields.Nested("CategorySchema", only=('name',))
    # brand = fields.Nested("BrandSchema", only=('name',))
    # employee = fields.Nested("EmployeeSchema", only=('id', 'name', 'is_admin',))
    
    

    
