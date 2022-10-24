from db import db, ma

class Brand(db.Model):
    __tablename__ = 'brands'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    country = db.Column(db.String(20), nullable=False)
    
    cars = db.relationship(
        "Car",
        backref='brand',
        cascade='all, delete'
    )

class BrandSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "country")