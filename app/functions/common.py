
from fastapi import HTTPException
from fastapi import status

from sqlalchemy import select

from sqlalchemy.engine import Result


async def execute_commit(model, db):

    db.add(model)
    await db.commit()
    await db.refresh(model)
    return model

