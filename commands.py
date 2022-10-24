from models.categories import Category
from models.employees import Employee
from models.brands import Brand
from models.cars import Car
from db import db, bcrypt
from flask import Blueprint
from datetime import datetime

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
            username = 'boss',
            password = bcrypt.generate_password_hash('boss123').decode('utf8'),
            name = 'Lee',
            is_admin = True
        ),
        Employee(
            username = 'employee1',
            password = bcrypt.generate_password_hash('employee1123').decode('utf8'),
            name = 'Billy'
        )
    ]
    db.session.add_all(employees)

    brands = [
        Brand(
            name = 'JEEP',
            country = "USA"
        ),
        Brand(
            name = 'Toyota',
            country = "Japan"
        )
    ]
    db.session.add_all(brands)

    categories = [
        Category(
            name = 'SUV'
        ),
        Category(
            name = 'Sports Car'
        )
    ]
    db.session.add_all(categories)
    db.session.commit()

    cars = [
        Car(
            category = categories[0],
            brand = brands[0],
            employee = employees[1],
            name = "Wrangler",
            price = 90000,
            is_offroad = True,
            year = 2022,
            km = 0
        ),

        Car(
            category = categories[1],
            brand = brands[1],
            employee = employees[1],
            name = "Supra",
            price = 100000,
            year = 2020,
            km = 23000
        )
    ]
    db.session.add_all(cars)
    db.session.commit()
    print("Table seeded")