from db import db, ma
from marshmallow.validate import OneOf

class Model(db.Model):
    __tablename__ = 'models'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    year = db.Column(db.Integer)
    
    brand_id = db.Column(db.Integer, db.ForeignKey("brands.id"), nullable=False)

    cars = db.relationship(
        "Car",
        backref="model"
    )

class ModelSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'brand_id', 'name', 'year')