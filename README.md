# Solved problems

## Functionality

This API is built to serve used car sales industries as a vehicles management system that can be utilized internally.  
The key problems to be solved in terms of functionality were:

1. Employee registration
    - To grant access to the system.
    - To assign vehicles.
2. Enabling to manage employees' personal information
    - In case of resignation or change in personal information.
3. Managing stocks
    - To track the vehicles they have.
    - To assign vehicles to dealers.
4. Assigning vehicles to the dealers
    - So dealers can check which vehicles have been assigned to them with other necessary information.
    - To track status of the vehicle for further management and decision. (please check the next section for more information)


The main function of this API is allowing managers to assign vehicles to dealers and dealers can check which vehicles have been assigned to them.  
It provides following information :

- A responsible employee for the assignment.
- A vehicle that has been assigned.
- Assigned date.
  - Automatically applied today's date when creating new record or when re-assigning an existing record to another employee.
- A goal date to sell before.
- Status (Ongoing/Overdue/Sold).
  - Default value is set to 'Ongoing' on creation.
  - *<u>*Designed to interact with the sale goal date.*</u>
  - Dealers only can change this value to 'Sold'.

'*' : *By entering a specific endpoint, all status values for all records that have expired sale goal dates and 'Ongoing' status values, can be updated to have 'Overdue' status values automatically at once.*  

Also, managers can filter the records by the status. For example if a manager apply 'Sold' filter, it shows only sold vehicles.  
Then, manager can delete the sold vehicles records from the stock and the corresponding assigned vehicle record will be deleted automatically together.

## Authentication & Authorization

Authentication verifies who you are. This problem should be solved to authorize individual users to have own/common access to particular resource.  
Authorization determines what you can access and what you can do. This problem should be solved to protect data.  

The problems have been solved by:

1. Distinguishing between registered employees and outsiders.
    - To not allow outsiders accessing to the system.
2. Verifying shared office password before employee registration.
    - To prevent outsiders registering in the system.
3. Distinguishing employees individually.
    - To prevent a (some) particular employee accessing to not related data.
    - For example, an employee does not need to manipulate the other employees' assigned vehicles data or personal information.
4. Distinguishing between 'manager' and 'employee'.
    - To provide different authorization.
    - For example, only managers are authorized to assign vehicles.

<hr>

# Used third party services

## flask

Flask is a Python module that is used as an web framework.  
It's a microframework that doesn't include an ORM.  

Main usages in this API :

- Generate url routes
- Generate and register blueprints
- Generate cli commands
- Raise error with custom error message by using `abort`
- Catch error by using `@app.errorhandler()`
- Receive request body by using `request.json`
- Set the app's configurations by using `app.config`

## flask-sqlalchemy

Sqlalchemy is an ORM (Object Relational Mapper) written in Python.  
By replacing the sql in the source code, it can prevent SQL injection.  
Sqlalchemy is cross-platform so it works with any other DBMS.

Main usages in this API:

- Creating/deleting tables
- Adding constraints
- Seeding data into tables
- Extracting data with and without filtering
- Raising `IntegrityError` for error handling

## marshmallow-sqlalchemy, flask-marshmallow

Marshmallow is a Python package that converts complex data types to Python data types or vice versa.  
It also offers powerful validation and customization features.

Main usages in this API:

- Validating request inputs
- Customizing response by defining `fields` and using `fields.Nested` in the model schema.
- Raising `ValidationError` with custom error message
- Converting Python data types to Json and vice versa

## flask-jwt-extended

jwt-extended is a Python package that is used for user authentication by generating Json Web Token that includes user's identity.  
Since jwt includes user's identity, developers can extract it and utilize it for authentication.  

Main usages in this API:

- Generating JWT for every employee registration.
- Authenticating employees for every access by requiring to pass their JWT.
- Extracting employees' id from jwt and utilize it to get relative records.

## psycopg2

It provides a connection between the DBMS and the app by defining a ```DATABASE_URL```.  
Same usage is applied in this app for connecting postgresql. 

The syntax is as follow to create a connection:  
```DATABASE_URL = "{dbms_name}+psycopg2://{db_username}:{db_user_password}@{IP_address}:{db_port}/{db_name}"```

## flask-bcrypt

It's a flask extension that provide bcrypt hashing function.  
It's used for hashing every employees' passwords in this app.  

The syntax is as follow to hash:  
```bcrypt.generate_password_hash({field_to_hash}).decode('utf8')```

## python-dotenv

It's a Python module that allows developers to have a separate `.env` file in the Python project directory to set environment variables.  
Environment variables must be defined in the form of `key=value` pairs.   

It provides following benefits while developing:

- Concealing secretes such as secrete key for JWT
- Easier to define own environment when the project is shared.

Usages in this app:

- Defining a secrete key for the JWT.
- Defining a shared office password for employees registration.
- Defining a database url.

## os

It's a Python module that can access to the operating system and extract environment variables.  

It can call environment variables in the other file without importing by using ```os.environ.get('{key}')```  

Usages in this app:

- Calling jwt secrete key.
- Calling office shared password.
- Calling database url.

## datetime

It's a python standard library that is only a single module.  
It can create date and time objects.

Usages in this app:

- Generating current date for certain model's column
- Setting the jwt's expiry time
- Setting the marshmallow validation condition for certain model's column.
