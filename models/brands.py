from db import db, ma

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
        fields = ("id", "name")