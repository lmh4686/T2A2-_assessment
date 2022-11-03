from wsgiref import validate
from init import db, ma
from marshmallow.validate import Regexp, Range, And, Length


class Stock(db.Model):
    __tablename__ = 'stocks'

    id = db.Column(db.Integer, primary_key=True)
    rego = db.Column(db.String(7), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    driven_km = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(10), nullable=False)
    
    trim_id = db.Column(db.Integer, db.ForeignKey("trims.id"), nullable=False)
    
    assigned_vehicle = db.relationship("AssignedVehicle",  
                                       back_populates='stock', 
                                       cascade="all, delete",
                                       uselist=False)
    trim = db.relationship("Trim",  back_populates='stocks')
    
    

class StockSchema(ma.Schema):
    class Meta:
        ordered = True 
        fields = ('id', 'rego', 'trim_id', 'price', 'driven_km', 'color')

    rego = ma.String(validate=And(Regexp('^[A-Z0-9]+$', 
                                         error='Only capital letters and numbers are allowed.'),
                                  Length(min=1, max=7)))
    
    trim_id = ma.Integer(validate=Range(min=1))
    
    price = ma.Integer(validate=Range(min=1000))
    
    driven_km = ma.Integer(validate=Range(min=10))
    
    color = ma.String(validate=And(Regexp('^[a-zA-Z]+$', 
                                          error='Must be only one word English alphabets.'),
                                   Length(min=2)))
    
    

    
