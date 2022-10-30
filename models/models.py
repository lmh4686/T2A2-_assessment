from init import db, ma
from marshmallow.validate import And, Regexp, Length

class Model(db.Model):
    __tablename__ = 'models'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    trim = db.Column(db.String(20), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(15), nullable=False)
    
    brand_id = db.Column(db.Integer, db.ForeignKey("brands.id"), nullable=False)
    body_id = db.Column(db.Integer, db.ForeignKey("bodies.id"), nullable=False)
    
    cars = db.relationship(
        "Car",
        backref="model"
    )

class ModelSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'brand_id', 'car_id', 'name', 'trim', 'year', 'color')
        
    color = ma.String(validate=And(Length(min=2, max=15), 
                                   Regexp('^[a-zA-Z]+$', 
                                          error= "Must be only English alphabets")))
    
    