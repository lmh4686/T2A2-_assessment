from init import db

def data_retriever(model, id=None):
    if id:
        obj = db.session.execute(db.select(model).filter_by(id=id)).scalar()
        return obj
    obj = db.session.execute(db.select(model)).scalars()
    return obj


    