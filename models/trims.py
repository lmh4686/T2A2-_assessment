from init import db, ma
from marshmallow.validate import Length, And, Regexp, OneOf, Range
from marshmallow import fields

VALID_TYPES = ("Suv", "Ute", "Sedan", "Wagon", "Convertible", "Hatch", "Coupe", "Van")

class Trim(db.Model):
    __tablename__ = 'trims'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable = False)
    body_type = db.Column(db.String(11), nullable=False)
    
    model_id = db.Column(db.Integer, db.ForeignKey("models.id"), nullable=False)
    
    stocks = db.relationship("Stock",  back_populates='trim')

class TrimSchema(ma.Schema):
    model = fields.Nested('ModelSchema', only=['name', 'year', 'brand'])
    class Meta:
        ordered = True
        fields = ("id", "name", "body_type", "model_id", "model")
            
    body_type = ma.String(validate=OneOf(VALID_TYPES))
    name = ma.String(validate=And(Length(min=2, max=20),
                                  Regexp('^[a-zA-Z0-9 ]+$', 
                                         error='Only English letters, numbers, space allowed')))
    model_id = ma.Integer(validate=Range(min=1))

    