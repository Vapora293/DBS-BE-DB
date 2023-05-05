import sqlalchemy.exc
from fastapi import APIRouter, HTTPException
from fastapi import Body

from sqlalchemy import insert, select, update, delete
from sqlalchemy.exc import IntegrityError

from pydantic import ValidationError
from sqlalchemy.orm import Session

from dbs_assignment import schemas
from dbs_assignment.config import engine
from dbs_assignment.models import Author, Category, Publication
from dbs_assignment.schemas import PublicationOut, PublicationCreate, AuthorSchema, CategorySchema
from typing import Any
import uuid

router = APIRouter()


@router.post("/publications", response_model=PublicationOut)
def create_publication(payload: dict = Body(...)):
    try:
        publication = schemas.PublicationCreate(**payload)
    except ValidationError:
        raise HTTPException(status_code=400)
    with Session(engine) as session:
        # Get authors
        authors = [
            session.query(Author).filter_by(name=author_data.name, surname=author_data.surname).one_or_none()
            for author_data in publication.authors
        ]
        if None in authors:
            raise HTTPException(status_code=400)

        # Get categories
        categories = [
            session.query(Category).filter_by(name=category_name).one_or_none()
            for category_name in publication.categories
        ]
        if None in categories:
            raise HTTPException(status_code=400)

        # Create publication
        new_publication = Publication(id=publication.id, title=publication.title, authors=authors,
                                      categories=categories)
        try:
            session.add(new_publication)
            session.commit()
            session.refresh(new_publication)
        except IntegrityError as e:
            session.rollback()
            if "duplicate key value violates unique constraint" in str(e):
                raise HTTPException(status_code=409)
            else:
                raise HTTPException(status_code=400)
        # Create the response object using the PublicationOut schema
        response = PublicationOut(
            id=new_publication.id,
            title=new_publication.title,
            authors=[AuthorSchema(id=author.id, name=author.name, surname=author.surname) for author in
                     new_publication.authors],
            categories=[CategorySchema(id=category.id, name=category.name) for category in new_publication.categories]
        )
    return response


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
