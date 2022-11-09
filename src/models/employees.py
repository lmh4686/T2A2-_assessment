from init import db, ma
from marshmallow.validate import Length, Email, Regexp, And
from marshmallow import validates
from marshmallow.exceptions import ValidationError


name_constraints = ma.String(validate=Regexp(
        '^[a-zA-Z]+$', 
        error="Only accept English alphabets"
        ))

class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    f_name = db.Column(db.String, nullable=False)
    l_name = db.Column(db.String, nullable=False)
    ph = db.Column(db.String(10), unique=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    
    assigned_vehicles = db.relationship("AssignedVehicle", back_populates="employee", cascade="all, delete")
                
        
class EmployeeSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "username", "password", "f_name", "l_name", "ph", "is_admin")        
        load_only = ["password"]
        
    username = ma.String(validate=Email())
    password = ma.String(validate=Length(min=6))
    f_name = name_constraints
    l_name = name_constraints
    @validates('ph')
    def validate_ph(self, value):
        if value[0] != '0':
            raise ValidationError("Must start from 0")
    ph = ma.String(validate=And(
        Length(equal=10, error= "Must be 10 digits"),
        Regexp('^[0-9]+$', error= "Must only contain 0-9 without space")
    ))
    
    