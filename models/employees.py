from db import db, ma
from marshmallow.validate import Length
from marshmallow import fields

class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean(), default=False)

    cars = db.relationship(
        "Car",
        backref="employee",
        cascade="all, delete"
    )

class EmployeeSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "username", "password", "name", "is_admin")
        load_only = ["password"]
    password = ma.String(validate=Length(min=6))