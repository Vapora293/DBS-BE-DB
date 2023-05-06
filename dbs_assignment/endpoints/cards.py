from fastapi import Body, APIRouter, HTTPException

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, DataError

from pydantic import ValidationError

from dbs_assignment import schemas
from dbs_assignment.config import engine
from dbs_assignment.models import Card
from dbs_assignment.endpoints.connection import session_scope

import uuid

from dbs_assignment.schemas import CardOut

router = APIRouter()


def card_return(new_card):
    return CardOut(
        id=new_card.id,
        user_id=new_card.user_id,
        magstripe=new_card.magstripe,
        status=new_card.status,
        created_at=new_card.created_at,
        updated_at=new_card.updated_at
    )


@router.post("/cards", status_code=201)
def create_card(payload: dict = Body(...)):
    if 'id' not in payload:
        payload['id'] = str(uuid.uuid4())
    try:
        card_schema = schemas.CardSchema(**payload)
    except ValidationError:
        raise HTTPException(status_code=400)

    new_card = Card(id=card_schema.id, user_id=card_schema.user_id, magstripe=card_schema.magstripe,
                    status=card_schema.status)
    with Session(engine) as session:
        try:
            session.add(new_card)
            session.commit()
            session.refresh(new_card)
        except IntegrityError as e:
            session.rollback()
            if "duplicate key value violates unique constraint" in str(e):
                raise HTTPException(status_code=409)
            else:
                raise HTTPException(status_code=400)
        except LookupError:
            session.rollback()
            raise HTTPException(status_code=400)

        return card_return(new_card)


@router.get("/cards/{card_id}", status_code=200)
def get_card(card_id: str):
    with Session(engine) as session:
        result = (
            session.query(Card).filter(Card.id == card_id).one_or_none()
        )
        if not result:
            raise HTTPException(status_code=404)

    return card_return(result)


@router.patch("/cards/{card_id}", status_code=200)
def update_card(card_id: str, payload: dict = Body(...)):
    try:
        card_schema = schemas.CardUpdateSchema(**payload)
    except ValidationError:
        raise HTTPException(status_code=400)

    with session_scope() as session:
        card = session.query(Card).filter(Card.id == card_id).one_or_none()
        if not card:
            raise HTTPException(status_code=404)
        for key, value in card_schema.dict().items():
            if value is not None:
                setattr(card, key, value)
        try:
            session.add(card)
            session.commit()
            session.refresh(card)
        except IntegrityError as e:
            session.rollback()
            if "duplicate key value violates unique constraint" in str(e):
                raise HTTPException(status_code=409)
            else:
                raise HTTPException(status_code=400)
        except DataError:
            session.rollback()
            raise HTTPException(status_code=400)

        return card_return(card)

@router.delete("/cards/{card_id}", status_code=204)
def delete_card(card_id: str):
    with session_scope() as session:
        card = session.query(Card).filter(Card.id == card_id).one_or_none()
        if not card:
            raise HTTPException(status_code=404)

        session.delete(card)
        session.commit()
    return None
