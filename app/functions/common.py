
async def execute_commit(model, db):

    db.add(model)
    db.commit()
    db.refresh(model)
    return model

