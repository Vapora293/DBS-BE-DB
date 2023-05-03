import sqlalchemy.exc
from fastapi import APIRouter, HTTPException
from fastapi import Body

from sqlalchemy import insert, select, update, delete
from sqlalchemy.exc import IntegrityError

from pydantic import ValidationError

from dbs_assignment import schemas
from dbs_assignment.config import engine
from dbs_assignment.models import Author, Category
from typing import Any
import uuid

router = APIRouter()


@router.post("/publications")
async def create_publication(payload: schemas.Publication):
    return payload


def sql_execution(fetching, deleteFlag=False):
    try:
        with engine.connect() as conn:
            result = conn.execute(fetching)
            conn.commit()
            if deleteFlag is True:
                return result.rowcount
    except sqlalchemy.exc.DataError:
        raise HTTPException(status_code=400)
    return result.fetchone()


def author_return(record):
    return {
        "id": record[0],
        "name": record[1],
        "surname": record[2],
        "createdAt": record[3],
        "updatedAt": record[4]
    }


@router.post("/authors", status_code=201)
def create_author(payload: dict = Body(...)) -> Any:
    try:
        author_schema = schemas.AuthorSchema(**payload)
    except ValidationError:
        raise HTTPException(status_code=400)

    if author_schema.id is None:
        author_schema.id = str(uuid.uuid4())
    author_data = author_schema.dict()

    try:
        fetching = insert(Author).values(**author_data).returning(Author.id, Author.name, Author.surname,
                                                                  Author.createdAt, Author.updatedAt)
        record = sql_execution(fetching)
    except IntegrityError:
        raise HTTPException(status_code=409)

    return author_return(record)


@router.get("/authors/{author_id}", status_code=200)
def get_author(author_id: str):
    fetching = select(Author).where(Author.id == author_id)
    record = sql_execution(fetching)
    if not record:
        raise HTTPException(status_code=404)

    return author_return(record)


@router.patch("/authors/{author_id}", status_code=200)
def update_author(author_id: str, payload: schemas.AuthorUpdateSchema) -> Any:
    update_data = payload.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400)
    fetching = update(Author).where(Author.id == author_id).values(**update_data).returning(Author.id, Author.name,
                                                                                            Author.surname,
                                                                                            Author.createdAt,
                                                                                            Author.updatedAt)

    return author_return(sql_execution(fetching))


@router.delete("/authors/{author_id}", status_code=204)
def delete_author(author_id: str):
    fetching = delete(Author).where(Author.id == author_id)
    result = sql_execution(fetching, True)
    if result == 0:
        raise HTTPException(status_code=400)
    return None


def category_return(record):
    return {
        "id": record[0],
        "name": record[1],
        "createdAt": record[2],
        "updatedAt": record[3]
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
                                                                      Category.createdAt, Category.updatedAt)
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
                                                                                                  Category.createdAt,
                                                                                                  Category.updatedAt)

    return category_return(sql_execution(fetching))


@router.delete("/categories/{category_id}", status_code=204)
def delete_author(category_id: str):
    fetching = delete(Category).where(Category.id == category_id)
    result = sql_execution(fetching, True)
    if result == 0:
        raise HTTPException(status_code=400)
    return None
