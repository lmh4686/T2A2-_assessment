from init import db
from flask import abort

def data_retriever(model, id=None):
    if id==0:
        abort(400, "id must be a natural number")
    if id :
        # From the given model, extract a record that has the same id with the given id in the parameter
        # query statement & execution all in one
        record = db.session.execute(db.select(model).filter_by(id=id)).scalar()
        return record
    # From the given model, extract all records. 
    records = db.session.execute(db.select(model)).scalars()
    return records
    
    