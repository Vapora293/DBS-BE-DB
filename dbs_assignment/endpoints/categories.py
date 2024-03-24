from fastapi import Body, APIRouter, HTTPException

from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert, select, update, delete

from pydantic import ValidationError
from sqlalchemy.orm import Session

from dbs_assignment import schemas
from dbs_assignment.config import engine
from dbs_assignment.models import Category
from dbs_assignment.endpoints.connection import sql_execution

from typing import Any
import uuid

from dbs_assignment.schemas import CategoryOut

router = APIRouter()


def proper_category_return(record):
    return CategoryOut(id=record.id, name=record.name, created_at=record.created_at, updated_at=record.updated_at)


def category_return(record):
    try:
        record[0]
    except:
        raise HTTPException(status_code=400)
    return {
        "id": record[0],
        "name": record[1],
        "created_at": record[2],
        "updated_at": record[3]
    }


@router.post("/categories", status_code=201)
def create_category(payload: dict = Body(...)) -> Any:
    if 'id' not in payload:
        payload['id'] = str(uuid.uuid4())
    try:
        category_schema = schemas.CategorySchema(**payload)
    except ValidationError:
        raise HTTPException(status_code=400)

    with Session(engine) as session:
        new_category = Category(id=category_schema.id, name=category_schema.name)
        try:
            session.add(new_category)
            session.commit()
            session.refresh(new_category)
        except IntegrityError:
            raise HTTPException(status_code=409)

    return proper_category_return(new_category)


@router.get("/categories/{category_id}", status_code=200)
def get_category(category_id: str):
    fetching = select(Category).where(Category.id == category_id)
    record = sql_execution(fetching)
    if not record:
        raise HTTPException(status_code=404)

    return category_return(record)


@router.patch("/categories/{category_id}", status_code=200)
def update_category(category_id: str, payload: dict = Body(...)) -> Any:
    try:
        category_schema = schemas.CategoryUpdateSchema(**payload)
    except ValidationError:
        raise HTTPException(status_code=400)
    if not category_schema:
        raise HTTPException(status_code=400)
    with Session(engine) as session:
        category = session.query(Category).filter(Category.id == category_id).one_or_none()
        if not category:
            raise HTTPException(status_code=404)

        for key, value in category_schema.dict().items():
            if value is not None:
                setattr(category, key, value)
        session.add(category)
        session.commit()
        session.refresh(category)

        return proper_category_return(category)


@router.delete("/categories/{category_id}", status_code=204)
def delete_category(category_id: str):
    fetching = delete(Category).where(Category.id == category_id)
    result = sql_execution(fetching, True)
    if result == 0:
        raise HTTPException(status_code=400)
    return None
