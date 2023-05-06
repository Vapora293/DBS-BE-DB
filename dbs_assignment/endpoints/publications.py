import uuid

from fastapi import APIRouter, HTTPException
from fastapi import Body

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from pydantic import ValidationError

from dbs_assignment import schemas
from dbs_assignment.config import engine
from dbs_assignment.endpoints.connection import session_scope
from dbs_assignment.models import Author, Category, Publication
from dbs_assignment.schemas import PublicationOut, AuthorSchema

router = APIRouter()


def publication_return(new_publication):
    return PublicationOut(
        id=new_publication.id,
        title=new_publication.title,
        authors=[{"name": author.name, "surname": author.surname} for author in
                 new_publication.authors],
        categories=[category.name for category in new_publication.categories],
        created_at=new_publication.created_at,
        updated_at=new_publication.updated_at
    )


@router.post("/publications", response_model=PublicationOut, status_code=201)
def create_publication(payload: dict = Body(...)):
    if 'id' not in payload:
        payload['id'] = str(uuid.uuid4())
    try:
        publication = schemas.PublicationSchema(**payload)
    except ValidationError:
        raise HTTPException(status_code=400)
    with Session(engine) as session:
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
            authors=[{"name": author.name, "surname": author.surname} for author in
                     new_publication.authors],
            categories=[category.name for category in new_publication.categories],
            created_at=new_publication.created_at,
            updated_at=new_publication.updated_at
        )
    return response


@router.get("/publications/{publication_id}", response_model=PublicationOut)
def get_publication(publication_id: str):
    with Session(engine) as session:
        result = (
            session.query(Publication)
            .options(joinedload(Publication.authors), joinedload(Publication.categories))
            .filter(Publication.id == publication_id).one_or_none()
        )
        if not result:
            raise HTTPException(status_code=404)

    return publication_return(result)


@router.patch("/publications/{publication_id}", response_model=PublicationOut)
def update_publication(publication_id: str, payload: dict = Body(...)):
    payload['id'] = publication_id
    try:
        payload_schema = schemas.PublicationSchema(**payload)
    except ValidationError:
        raise HTTPException(status_code=400)
    with session_scope() as session:
        publication = session.query(Publication).filter(Publication.id == publication_id).one_or_none()
        if not publication:
            raise HTTPException(status_code=404)

        authors = [
            session.query(Author).filter_by(name=author_data.name, surname=author_data.surname).one_or_none()
            for author_data in payload_schema.authors
        ]
        if None in authors:
            raise HTTPException(status_code=400)
        publication.authors = authors

        categories = [
            session.query(Category).filter_by(name=category_name).one_or_none()
            for category_name in payload_schema.categories
        ]
        if None in categories:
            raise HTTPException(status_code=400)
        publication.categories = categories
        session.refresh(publication)

        return publication_return(publication)


@router.delete("/publications/{publication_id}", status_code=204)
def delete_publication(publication_id: str):
    with session_scope() as session:
        publication = session.query(Publication).filter(Publication.id == publication_id).one_or_none()
        if not publication:
            raise HTTPException(status_code=404)

        session.delete(publication)
        session.commit()
    return None
