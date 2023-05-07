from fastapi import Body, APIRouter, HTTPException

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from pydantic import ValidationError

from dbs_assignment import schemas
from dbs_assignment.config import engine
from dbs_assignment.endpoints.connection import session_scope
from dbs_assignment.models import User, Rental

import uuid

from dbs_assignment.schemas import UserOut, RentalOut

router = APIRouter()

##TODO tu mam lepsiu verziu patch requestu

def rental_to_rental_out(rental: Rental) -> RentalOut:
    return RentalOut(
        id=rental.id,
        user_id=rental.user_id,
        publication_instance_id=rental.publication_instance_id,
        duration=rental.duration,
        start_date=rental.start_date,
        end_date=rental.end_date,
        status=rental.status
    )


def user_return(new_user):
    with Session(engine) as session:
        rentals = session.query(Rental).filter(Rental.user_id == new_user.id)
        rental_out_list = [rental_to_rental_out(rental) for rental in rentals]
        if len(rental_out_list) == 0:
            return UserOut(
                id=new_user.id,
                name=new_user.name,
                surname=new_user.surname,
                email=new_user.email,
                birth_date=new_user.birth_date,
                personal_identificator=new_user.personal_identificator,
                created_at=new_user.created_at,
                updated_at=new_user.updated_at,
            ).dict(exclude_unset=True)
        return UserOut(
            id=new_user.id,
            name=new_user.name,
            surname=new_user.surname,
            email=new_user.email,
            birth_date=new_user.birth_date,
            personal_identificator=new_user.personal_identificator,
            rentals=rental_out_list,
            created_at=new_user.created_at,
            updated_at=new_user.updated_at,
        ).dict(exclude_unset=True)


@router.post("/users", status_code=201)
def create_user(payload: dict = Body(...)):
    if 'id' not in payload:
        payload['id'] = str(uuid.uuid4())
    try:
        user_schema = schemas.UserSchema(**payload)
    except ValidationError:
        raise HTTPException(status_code=400)


    with Session(engine) as session:
        new_user = User(id=user_schema.id, name=user_schema.name, surname=user_schema.surname, email=user_schema.email,
                        birth_date=user_schema.birth_date, personal_identificator=user_schema.personal_identificator)
        try:
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
        except IntegrityError as e:
            session.rollback()
            if "duplicate key value violates unique constraint" in str(e):
                raise HTTPException(status_code=409, detail="Email already taken")
            else:
                raise HTTPException(status_code=400)

        return user_return(new_user)



@router.get("/users/{user_id}", status_code=200)
def get_user(user_id: str):
    with Session(engine) as session:
        result = (
            session.query(User).filter(User.id == user_id).one_or_none()
        )
        rentals = (session.query(Rental).filter(Rental.user_id == user_id))
        rental_out_list = [rental_to_rental_out(rental) for rental in rentals]
        if not result:
            raise HTTPException(status_code=404)
    return user_return(result)


@router.patch("/users/{user_id}", status_code=200)
def update_user(user_id: str, payload: dict = Body(...)):
    try:
        user_schema = schemas.UserUpdateSchema(**payload)
    except ValidationError:
        raise HTTPException(status_code=400)

    with session_scope() as session:
        user = session.query(User).filter(User.id == user_id).one_or_none()
        if not user:
            raise HTTPException(status_code=404)

        # Update user attributes with the new values
        for key, value in user_schema.dict().items():
            if value is not None:
                setattr(user, key, value)

        session.add(user)  # Mark the user object as dirty to update the record
        session.commit()   # Commit the changes to the database
        session.refresh(user)

        return user_return(user)


