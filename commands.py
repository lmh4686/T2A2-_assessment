from models.models import Model
from models.employees import Employee
from models.brands import Brand
from models.bodies import Body
from models.cars import Car
from models.assigned_cars import AssignedCar
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
    
    bodies = [
        Body(
            type = 'Suv',
            size = 'Medium',          
        ),
        Body(
            type = 'Ute',
            size = 'Medium',          
        )
    ]
    db.session.add_all(bodies)
    db.session.commit()

    models = [
        Model(
            brand = brands[0],
            body = bodies[0],
            name = "Wrangler",
            trim = "Unlimited Rubicon",
            year = 2022,
            color = 'Black'
        ),

        Model(
            brand = brands[1],
            body = bodies[1],
            name = "Hilux",
            trim = "Rugged X",
            year = 2019,
            color = 'White'
        )
    ]
    db.session.add_all(models)
    db.session.commit()
    
    cars = [
        Car(
            model = models[0],
            rego = '1PK8GO',
            price = 90599,
            driven_km = 3520
        ),
        Car(
            model = models[1],
            rego = '3JN8CU',
            price = 71400,
            driven_km = 37621
        )
    ]
    db.session.add_all(cars)
    db.session.commit()
    
    assigned_cars = [
        AssignedCar(
            emp_id = employees[1].id,
            car_id = cars[0].id,
            sale_goal_date = datetime.strptime('15 Dec 2022', '%d %b %Y'),
            assigned_date = date.today(),
            status = 'Ongoing'
        ),
        AssignedCar(
            emp_id = employees[1].id,
            car_id = cars[1].id,
            sale_goal_date = datetime.strptime('15 Jan 2023', '%d %b %Y'),
            assigned_date = date.today(),
            status = 'Ongoing'
        )
    ]
    db.session.add_all(assigned_cars)
    db.session.commit()
    
    print("Table seeded")