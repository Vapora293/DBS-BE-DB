from fastapi import Body, APIRouter, HTTPException

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from pydantic import ValidationError

from dbs_assignment import schemas
from dbs_assignment.config import engine
from dbs_assignment.endpoints.connection import session_scope
from dbs_assignment.models import User

import uuid

from dbs_assignment.schemas import UserOut

router = APIRouter()

##TODO tu mam lepsiu verziu patch requestu

def user_return(new_user):
    return UserOut(
        id=new_user.id,
        name=new_user.name,
        surname=new_user.surname,
        email=new_user.email,
        birth_date=new_user.birth_date,
        personal_identificator=new_user.personal_identificator,
        created_at=new_user.created_at,
        updated_at=new_user.updated_at
    )


@router.post("/users", status_code=201)
def create_user(payload: dict = Body(...)):
    if 'id' not in payload:
        payload['id'] = str(uuid.uuid4())
    try:
        user_schema = schemas.UserSchema(**payload)
    except ValidationError:
        raise HTTPException(status_code=400)

    new_user = User(id=user_schema.id, name=user_schema.name, surname=user_schema.surname, email=user_schema.email,
                    birth_date=user_schema.birth_date, personal_identificator=user_schema.personal_identificator)

    with Session(engine) as session:
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


