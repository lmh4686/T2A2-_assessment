from init import db, ma
from marshmallow.validate import And, Regexp, Length, Range
from datetime import datetime
from marshmallow import fields

class Model(db.Model):
    __tablename__ = 'models'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    
    brand_id = db.Column(db.Integer, db.ForeignKey("brands.id"), nullable=False)
    
    trims = db.relationship(
        "Trim",
        backref="model"
    )

class ModelSchema(ma.Schema):
    brand = fields.Nested('BrandSchema', only=['name'])
    class Meta:
        ordered = True
        fields = ('id', 'name', 'year', 'brand_id', 'brand')
    
    # Exclude required=True for PUT/PATCH operations
    name = ma.String(validate=And(Length(min=2, max=20),
                                  Regexp('^[a-zA-Z0-9 ]+$', 
                                         error="Only English alphabets, numbers, space are allowed")))
    year = ma.Integer(validate=Range(min=1900, max=datetime.now().year + 1))
    brand_id = ma.Integer(validate=Range(min=1))
    
    

    