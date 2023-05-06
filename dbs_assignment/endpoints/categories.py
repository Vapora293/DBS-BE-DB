from fastapi import Body, APIRouter, HTTPException

from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert, select, update, delete

from pydantic import ValidationError

from dbs_assignment import schemas
from dbs_assignment.models import Category
from dbs_assignment.endpoints.connection import sql_execution

from typing import Any
import uuid

router = APIRouter()
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
    try:
        category_schema = schemas.CategorySchema(**payload)
    except ValidationError:
        raise HTTPException(status_code=400)

    if category_schema.id is None:
        category_schema.id = str(uuid.uuid4())
    category_data = category_schema.dict()

    try:
        fetching = insert(Category).values(**category_data).returning(Category.id, Category.name,
                                                                      Category.created_at, Category.updated_at)
        record = sql_execution(fetching)
    except IntegrityError:
        raise HTTPException(status_code=409)

    return category_return(record)


@router.get("/categories/{category_id}", status_code=200)
def get_category(category_id: str):
    fetching = select(Category).where(Category.id == category_id)
    record = sql_execution(fetching)
    if not record:
        raise HTTPException(status_code=404)

    return category_return(record)


@router.patch("/categories/{category_id}", status_code=200)
def update_category(category_id: str, payload: schemas.CategoryUpdateSchema) -> Any:
    update_data = payload.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400)
    fetching = update(Category).where(Category.id == category_id).values(**update_data).returning(Category.id,
                                                                                                  Category.name,
                                                                                                  Category.created_at,
                                                                                                  Category.updated_at)

    return category_return(sql_execution(fetching))


@router.delete("/categories/{category_id}", status_code=204)
def delete_author(category_id: str):
    fetching = delete(Category).where(Category.id == category_id)
    result = sql_execution(fetching, True)
    if result == 0:
        raise HTTPException(status_code=400)
    return None
