from init import db
from marshmallow.exceptions import ValidationError

def data_retriever(model, id=None):
    if id==0:
        raise ValidationError({"err": "id must be a natural number bigger than 0"})
    if id :
        # From the given model, extract a record that has the same id with the given id in the parameter
        # query statement & execution all in one
        obj = db.session.execute(db.select(model).filter_by(id=id)).scalar()
        return obj
    # From the given model, extract all records. 
    obj = db.session.execute(db.select(model)).scalars()
    return obj




    