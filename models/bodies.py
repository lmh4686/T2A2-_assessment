from init import db, ma
from marshmallow.validate import Length, And, Regexp, OneOf
from marshmallow import validates

VALID_TYPES = ("Suv", "Ute", "Sedan", "Wagon", "Convertible", "Hatch", "Coupe", "Van")
VALID_SIZES = ("Compact", "Small", "Medium", "Large")


class Body(db.Model):
    __tablename__ = 'bodies'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(11), nullable=False)
    size = db.Column(db.String(10), nullable=False)
    
    models = db.relationship(
        "Model",
        backref='body'
    )


class BodySchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "type", "size")
            
    type = ma.String(validate=OneOf(VALID_TYPES))
    size = ma.String(validate=OneOf(VALID_SIZES))

    