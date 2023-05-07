import datetime
import uuid

from fastapi import Body, APIRouter, HTTPException
from sqlalchemy import func

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from pydantic import ValidationError

from dbs_assignment import schemas
from dbs_assignment.config import engine
from dbs_assignment.schemas import RentalOut
from dbs_assignment.endpoints.connection import session_scope
from dbs_assignment.models import Rental, Instance, Reservation

router = APIRouter()


def rental_return(new_rental):
    return RentalOut(
        id=new_rental.id,
        user_id=new_rental.user_id,
        publication_instance_id=new_rental.publication_instance_id,
        duration=new_rental.duration,
        start_date=new_rental.start_date,
        end_date=new_rental.end_date,
        status=new_rental.status
    )


@router.post("/rentals", response_model=RentalOut, status_code=201)
def create_rental(payload: dict = Body(...)):
    if 'id' not in payload:
        payload['id'] = str(uuid.uuid4())
    try:
        if payload['duration'] < 0 or payload['duration'] > 14:
            raise HTTPException(status_code=400)
        rental = schemas.RentalSchema(**payload)
    except ValidationError:
        raise HTTPException(status_code=400)
    with Session(engine) as session:
        free_instance = session.query(Instance).filter(Instance.publication_id == rental.publication_id).filter(
            Instance.status == 'available').first()
        if not free_instance:
            raise HTTPException(status_code=400)
        reservations_for_instance = (
            session.query(Reservation)
            .filter(Reservation.publication_id == rental.publication_id)
            .order_by(Reservation.created_at.asc())
            .first()
        )
        if reservations_for_instance:
            if reservations_for_instance.user_id != rental.user_id:
                raise HTTPException(status_code=400)
        free_instance.status = 'reserved'
        session.commit()
        session.refresh(free_instance)
        if reservations_for_instance:
            raise HTTPException(status_code=400)
        new_rental = Rental(id=rental.id, user_id=rental.user_id, publication_instance_id=free_instance.id,
                            duration=rental.duration,
                            start_date=func.now(),
                            end_date=datetime.datetime.now() + datetime.timedelta(days=rental.duration))
        try:
            session.add(new_rental)
            session.commit()
            session.refresh(new_rental)
        except IntegrityError as e:
            session.rollback()
            if "duplicate key value violates unique constraint" in str(e):
                raise HTTPException(status_code=409)
            else:
                raise HTTPException(status_code=400)

    return rental_return(new_rental)


@router.get("/rentals/{rental_id}", response_model=RentalOut)
def get_rental(rental_id: str):
    with Session(engine) as session:
        result = (
            session.query(Rental).filter(Rental.id == rental_id).one_or_none()
        )
        if not result:
            raise HTTPException(status_code=404)

    return rental_return(result)


@router.patch("/rentals/{rental_id}", response_model=RentalOut)
def update_publication(rental_id: str, payload: dict = Body(...)):
    try:
        rental_schema = schemas.RentalUpdateSchema(**payload)
    except ValidationError:
        raise HTTPException(status_code=400)
    with session_scope() as session:
        rental = session.query(Rental).filter(Rental.id == rental_id).one_or_none()
        if not rental:
            raise HTTPException(status_code=404)
        if rental.status != 'active':
            raise HTTPException(status_code=400)
        rental.end_date += datetime.timedelta(days=rental_schema.duration)
        rental.duration += rental_schema.duration
        session.commit()
        session.refresh(rental)

        return rental_return(rental)
