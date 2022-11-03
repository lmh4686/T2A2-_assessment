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
            password = bcrypt.generate_password_hash('emp123').decode('utf8'),
            f_name = 'Billy',
            l_name = 'William',
            ph = '0987654210'
        ),
        Employee(
            username = 'emp2@email.com',
            password = bcrypt.generate_password_hash('emp2123').decode('utf8'),
            f_name = 'John',
            l_name = 'Wilson',
            ph = '0452365423'
        ),
        Employee(
            username = 'emp3@email.com',
            password = bcrypt.generate_password_hash('emp3123').decode('utf8'),
            f_name = 'Stuart',
            l_name = 'Park',
            ph = '0329846521'
        ),
        Employee(
            username = 'emp4@email.com',
            password = bcrypt.generate_password_hash('emp4123').decode('utf8'),
            f_name = 'John',
            l_name = 'Terry',
            ph = '0321367952'
        ),
        Employee(
            username = 'emp5@email.com',
            password = bcrypt.generate_password_hash('emp5123').decode('utf8'),
            f_name = 'Susan',
            l_name = 'Morgan',
            ph = '0846317955'
        ),
        Employee(
            username = 'emp6@gmail.com',
            password = bcrypt.generate_password_hash('emp6123').decode('utf8'),
            f_name = 'Phil',
            l_name = 'Robert',
            ph = '0645953457'
        ),
        
    ]
    db.session.add_all(employees)
    
    brands = [
        Brand(
            name = 'Jeep'
        ),
        Brand(
            name = 'Toyota'
        ),
        Brand(
            name = 'Ford'
        ),
        Brand(
            name = 'Bmw'
        ),
        Brand(
            name = 'Benz'
        ),
        Brand(
            name = 'Genesis'
        ),
        Brand(
            name = 'Mazda'
        ),
    ]
    db.session.add_all(brands)
    
    models = [
        Model(
            brand = brands[0],
            name = 'Wrangler',
            year = 2022         
        ),
        Model(
            brand = brands[0],
            name = 'Gladiator',
            year = 2017        
        ),
        Model(
            brand = brands[0],
            name = 'Grand cherokee',
            year = 2022         
        ),
        Model(
            brand = brands[1],
            name = 'Land cruiser',
            year = 2017        
        ),
        Model(
            brand = brands[1],
            name = 'Hilux',
            year = 2015        
        ),
        Model(
            brand = brands[1],
            name = 'Camry',
            year = 2013        
        ),
        Model(
            brand = brands[2],
            name = 'Bronco',
            year = 2009         
        ),
        Model(
            brand = brands[2],
            name = 'Ranger',
            year = 2012        
        ),
        Model(
            brand = brands[2],
            name = 'Everest',
            year = 2008         
        ),
        Model(
            brand = brands[2],
            name = 'Mustang',
            year = 2022        
        ),
        Model(
            brand = brands[3],
            name = 'X5',
            year = 2011         
        ),
        Model(
            brand = brands[3],
            name = 'Bmw 3',
            year = 2005        
        ),
        Model(
            brand = brands[3],
            name = 'Bmw 6',
            year = 2014         
        ),
        Model(
            brand = brands[4],
            name = 'Glc class',
            year = 2019        
        ),
        Model(
            brand = brands[4],
            name = 'A class',
            year = 2011         
        ),
        Model(
            brand = brands[4],
            name = 'C class',
            year = 2005        
        ),
        Model(
            brand = brands[5],
            name = 'G80',
            year = 2020         
        ),
        Model(
            brand = brands[5],
            name = 'Gv90',
            year = 2022        
        ),
        Model(
            brand = brands[5],
            name = 'G60',
            year = 2021        
        ),
        Model(
            brand = brands[6],
            name = 'Mazda 3',
            year = 2005        
        ),
        Model(
            brand = brands[6],
            name = 'Mazda 6',
            year = 2014         
        ),
        Model(
            brand = brands[6],
            name = 'Cx9',
            year = 2019
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
            model = models[0],
            name = 'Rubicon',
            body_type = 'Suv'
        ),
        Trim(
            model = models[0],
            name = 'Night eagle',
            body_type = 'Suv'
        ),
        Trim(
            model = models[1],
            name = 'Rubicon',
            body_type = 'Ute'
        ),
        Trim(
            model = models[2],
            name = 'L limited',
            body_type = 'Suv'
        ),
        Trim(
            model = models[2],
            name = 'L summit reserve',
            body_type = 'Suv'
        ),
        Trim(
            model = models[2],
            name = 'Night eagle',
            body_type = 'Suv'
        ),
        Trim(
            model = models[3],
            name = 'Gr sport',
            body_type = 'Suv'
        ),
        Trim(
            model = models[3],
            name = 'Gx',
            body_type = 'Suv'
        ),
        Trim(
            model = models[3],
            name = 'Sahara',
            body_type = 'Suv'
        ),
        Trim(
            model = models[4],
            name = 'Rugged x',
            body_type = 'Ute'
        ),
        Trim(
            model = models[4],
            name = 'Rouge',
            body_type = 'Ute'
        ),
        Trim(
            model = models[4],
            name = 'Sr',
            body_type = 'Ute'
        ),
        Trim(
            model = models[5],
            name = 'Ascent',
            body_type = 'Sedan'
        ),
        Trim(
            model = models[5],
            name = 'CSi',
            body_type = 'Sedan'
        ),
        Trim(
            model = models[1],
            name = 'Atara r',
            body_type = 'Sedan'
        ),
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
        ),
        Stock(
             trim = trims[3],
             rego = '1KN8PN',
             price = 65322,
             driven_km = 53520,
             color = 'Green'
        ),
        Stock(
             trim = trims[2],
             rego = '8MS3LS',
             price = 93561,
             driven_km = 376,
             color = 'Red'
        ),
        Stock(
             trim = trims[3],
             rego = '5LM2IR',
             price = 20874,
             driven_km = 190000,
             color = 'Green'
        ),
        Stock(
             trim = trims[4],
             rego = '9NB0KS',
             price = 15865,
             driven_km = 176211,
             color = 'Gray'
        ),
        Stock(
             trim = trims[5],
             rego = '8KJ2NZ',
             price = 52000,
             driven_km = 53520,
             color = 'Black'
        ),
        Stock(
             trim = trims[6],
             rego = '1NM52UD',
             price = 8999,
             driven_km = 237621,
             color = 'Beige'
        ),
        Stock(
             trim = trims[7],
             rego = '5MZ9QY',
             price = 23548,
             driven_km = 120000,
             color = 'Purple'
        ),
        Stock(
             trim = trims[8],
             rego = '5FJ9BX',
             price = 78500,
             driven_km = 37621,
             color = 'Sand'
        ),
        Stock(
             trim = trims[9],
             rego = '8BD8JD',
             price = 32500,
             driven_km = 23520,
             color = 'Blue'
        ),
        Stock(
             trim = trims[10],
             rego = '7BN1SL',
             price = 98520,
             driven_km = 23,
             color = 'White'
        ),
        Stock(
             trim = trims[11],
             rego = '8ND1VD',
             price = 12000,
             driven_km = 233520,
             color = 'Orange'
        ),
        Stock(
             trim = trims[12],
             rego = '5MC83S',
             price = 15300,
             driven_km = 57621,
             color = 'Grey'
        ),
        Stock(
             trim = trims[13],
             rego = '5MX8BX',
             price = 74900,
             driven_km = 23520,
             color = 'Black'
        ),
        Stock(
             trim = trims[14],
             rego = '5MN6HF',
             price = 45630,
             driven_km = 29850,
             color = 'Black'
        ),
    ]
    db.session.add_all(stocks)
    db.session.commit()
    
    assigned_vehicles = [
        AssignedVehicle(
            employee = employees[1],
            stock = stocks[0],
            sale_goal_date = datetime.strptime('15 Feb 2022', '%d %b %Y'),
            assigned_date = datetime.strptime('09 Dec 2021', '%d %b %Y'),
        ),
        AssignedVehicle(
            employee = employees[1],
            stock = stocks[1],
            sale_goal_date = datetime.strptime('15 Jan 2020', '%d %b %Y'),
            assigned_date = datetime.strptime('09 Nov 2021', '%d %b %Y'),
            status = 'Sold'
        ),
        AssignedVehicle(
            employee = employees[2],
            stock = stocks[2],
            sale_goal_date = datetime.strptime('05 Nov 2023', '%d %b %Y'),
            assigned_date = datetime.strptime('09 Oct 2022', '%d %b %Y')
        ),
        AssignedVehicle(
            employee = employees[3],
            stock = stocks[3],
            sale_goal_date = datetime.strptime('25 Mar 2020', '%d %b %Y'),
            assigned_date = datetime.strptime('09 Feb 2020', '%d %b %Y'),
            status = 'Sold'
        ),
        AssignedVehicle(
            employee = employees[3],
            stock = stocks[4],
            sale_goal_date = datetime.strptime('14 Nov 2022', '%d %b %Y'),
            assigned_date = datetime.strptime('09 Oct 2022', '%d %b %Y')
        ),
        AssignedVehicle(
            employee = employees[4],
            stock = stocks[5],
            sale_goal_date = datetime.strptime('15 Mar 2022', '%d %b %Y'),
            assigned_date = datetime.strptime('09 Jan 2022', '%d %b %Y')
        )
    ]
    db.session.add_all(assigned_vehicles)
    db.session.commit()
    
    print("Table seeded")