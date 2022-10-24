from db import db, ma

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)

    cars = db.relationship(
        "Car",
        backref="category",
        cascade="all, delete"
    )

class CategorySchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')