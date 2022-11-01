from models.models import Model
from models.employees import Employee
from models.brands import Brand
from models.trims import Trim
from models.stocks import Stock
from models.assigned_vehicles import AssignedVehicle
from init import db, bcrypt
from flask import Blueprint
from datetime import datetime, date

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("Tables created")

@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables dropped")

@db_commands.cli.command("seed")
def seed_db():
    employees = [
        Employee(
            username = 'lmh4686@gmail.com',
            password = bcrypt.generate_password_hash('boss123').decode('utf8'),
            f_name = 'Jihyuk',
            l_name = 'Lee',
            ph = '0321476521',
            is_admin = True
        ),
        Employee(
            username = 'employee1@email.com',
            password = bcrypt.generate_password_hash('employee1123').decode('utf8'),
            f_name = 'Billy',
            l_name = 'William',
            ph = '0987654210'
        )
    ]
    db.session.add_all(employees)
    
    brands = [
        Brand(
            name = 'Jeep'
        ),
        Brand(
            name = 'Toyota'
        )
    ]
    db.session.add_all(brands)
    
    models = [
        Model(
            brand = brands[0],
            name = 'Wrangler',
            year = 2022         
        ),
        Model(
            brand = brands[1],
            name = 'Land Cruiser',
            year = 2017        
        )
    ]
    db.session.add_all(models)
    db.session.commit()

    trims = [
        Trim(
            model = models[0],
            name = 'Unlimited Rubicon',
            body_type = 'Suv'
        ),

        Trim(
            model = models[1],
            name = 'Sahara',
            body_type = 'Suv'
        )
    ]
    db.session.add_all(trims)
    db.session.commit()
    
    stocks = [
        Stock(
             trim = trims[0],
             rego = '1PK8GO',
             price = 90599,
             driven_km = 3520,
             color = 'Black'
        ),
        Stock(
             trim = trims[1],
             rego = '3JN8CU',
             price = 81400,
             driven_km = 37621,
             color = 'White'
        )
    ]
    db.session.add_all(stocks)
    db.session.commit()
    
    assigned_vehicles = [
        AssignedVehicle(
            employee = employees[1],
            stock = stocks[0],
            sale_goal_date = datetime.strptime('15 Dec 2022', '%d %b %Y'),
            assigned_date = date.today(),
            status = 'Ongoing'
        ),
        AssignedVehicle(
            employee = employees[1],
            stock = stocks[1],
            sale_goal_date = datetime.strptime('15 Jan 2023', '%d %b %Y'),
            assigned_date = date.today(),
            status = 'Ongoing'
        )
    ]
    db.session.add_all(assigned_vehicles)
    db.session.commit()
    
    print("Table seeded")