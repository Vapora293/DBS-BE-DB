import datetime
import uuid

from fastapi import Body, APIRouter, HTTPException
from sqlalchemy import func

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from pydantic import ValidationError

from dbs_assignment import schemas
from dbs_assignment.config import engine
from dbs_assignment.schemas import ReservationOut
from dbs_assignment.endpoints.connection import session_scope
from dbs_assignment.models import Reservation

router = APIRouter()


def reservation_return(new_reservation):
    return ReservationOut(
        id=new_reservation.id,
        user_id=new_reservation.user_id,
        publication_id=new_reservation.publication_id,
        created_at=new_reservation.created_at,
    )


@router.post("/reservations", response_model=ReservationOut, status_code=201)
def create_reservation(payload: dict = Body(...)):
    if 'id' not in payload:
        payload['id'] = str(uuid.uuid4())
    try:
        reservation = schemas.ReservationSchema(**payload)
    except ValidationError:
        raise HTTPException(status_code=400)
    with Session(engine) as session:
        new_reservation = Reservation(id=reservation.id, user_id=reservation.user_id, publication_id=reservation.publication_id)
        try:
            session.add(new_reservation)
            session.commit()
            session.refresh(new_reservation)
        except IntegrityError as e:
            session.rollback()
            if "duplicate key value violates unique constraint" in str(e):
                raise HTTPException(status_code=409)
            else:
                raise HTTPException(status_code=400)

    return reservation_return(new_reservation)


@router.get("/reservations/{reservation_id}", response_model=ReservationOut)
def get_reservation(reservation_id: str):
    with Session(engine) as session:
        result = (
            session.query(Reservation).filter(Reservation.id == reservation_id).one_or_none()
        )
        if not result:
            raise HTTPException(status_code=404)

    return reservation_return(result)


@router.delete("/reservations/{reservation_id}", status_code=204)
def delete_reservation(reservation_id: str):
    with session_scope() as session:
        reservation = session.query(Reservation).filter(Reservation.id == reservation_id).one_or_none()
        if not reservation:
            raise HTTPException(status_code=404)

        session.delete(reservation)
        session.commit()
    return None
