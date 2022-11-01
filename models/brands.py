from init import db, ma
from marshmallow.validate import Length, And, Regexp


class Brand(db.Model):
    __tablename__ = 'brands'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    
    models = db.relationship(
        "Model",
        backref='brand'
    )


class BrandSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "name")
    name = ma.String(required=True, 
                     validate=And(Length(min=2, max=20), 
                                  Regexp('^[a-zA-Z]+$', 
                                         error= "Must be only English alphabets")))