from fastapi import APIRouter, HTTPException
from fastapi import Body

from sqlalchemy import insert, select, update, delete
from sqlalchemy.exc import IntegrityError

from pydantic import ValidationError

from dbs_assignment import schemas
from dbs_assignment.endpoints.connection import sql_execution
from dbs_assignment.models import Author

from typing import Any
import uuid

router = APIRouter()
def author_return(record):
    try:
        record[0]
    except:
        raise HTTPException(status_code=400)
    return {
        "id": record[0],
        "name": record[1],
        "surname": record[2],
        "created_at": record[3],
        "updated_at": record[4]
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
                                                                  Author.created_at, Author.updated_at)
        record = sql_execution(fetching)
    except IntegrityError:
        raise HTTPException(status_code=409)

    return author_return(record)


@router.get("/authors/{author_id}", status_code=200)
def get_author(author_id: str):
    record = sql_execution(select(Author).where(Author.id == author_id))
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
                                                                                            Author.created_at,
                                                                                            Author.updated_at)

    return author_return(sql_execution(fetching))


@router.delete("/authors/{author_id}", status_code=204)
def delete_author(author_id: str):
    fetching = delete(Author).where(Author.id == author_id)
    result = sql_execution(fetching, True)
    if result == 0:
        raise HTTPException(status_code=400)
    return None



