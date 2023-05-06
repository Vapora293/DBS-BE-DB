from fastapi import Body, APIRouter, HTTPException

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from pydantic import ValidationError

from dbs_assignment import schemas
from dbs_assignment.config import engine
from dbs_assignment.models import Instance
from dbs_assignment.schemas import InstanceOut
from dbs_assignment.endpoints.connection import session_scope

import uuid


router = APIRouter()

##TODO osetrit pri patch requeste ked nedas vbc nic
def instance_return(instance):
    return InstanceOut(
        id=instance.id,
        type=instance.type,
        publisher=instance.publisher,
        year=instance.year,
        status=instance.status,
        publication_id=instance.publication_id,
        created_at=instance.created_at,
        updated_at=instance.updated_at
    )


@router.post("/instances", status_code=201)
def create_instance(payload: dict = Body(...)):
    if 'id' not in payload:
        payload['id'] = str(uuid.uuid4())
    try:
        instance_schema = schemas.InstanceSchema(**payload)
    except ValidationError:
        raise HTTPException(status_code=400)

    new_instance = Instance(id=instance_schema.id, type=instance_schema.type, publisher=instance_schema.publisher, year=instance_schema.year,
                    status=instance_schema.status, publication_id=instance_schema.publication_id)
    with Session(engine) as session:
        try:
            session.add(new_instance)
            session.commit()
            session.refresh(new_instance)
        except IntegrityError as e:
            session.rollback()
            if "duplicate key value violates unique constraint" in str(e):
                raise HTTPException(status_code=409)
            else:
                raise HTTPException(status_code=400)
        except LookupError:
            session.rollback()
            raise HTTPException(status_code=400)

        return instance_return(new_instance)


@router.get("/instances/{instance_id}", status_code=200)
def get_instance(instance_id: str):
    with Session(engine) as session:
        result = (
            session.query(Instance).filter(Instance.id == instance_id).one_or_none()
        )
        if not result:
            raise HTTPException(status_code=404)

    return instance_return(result)


@router.patch("/instances/{instance_id}", status_code=200)
def update_instance(instance_id: str, payload: dict = Body(...)):
    try:
        instance_schema = schemas.InstanceUpdateSchema(**payload)
    except ValidationError:
        raise HTTPException(status_code=400)

    with session_scope() as session:
        instance = session.query(Instance).filter(Instance.id == instance_id).one_or_none()
        if not instance:
            raise HTTPException(status_code=404)
        for key, value in instance_schema.dict().items():
            if value is not None:
                setattr(instance, key, value)
        try:
            session.add(instance)
            session.commit()
            session.refresh(instance)
        except IntegrityError as e:
            session.rollback()
            if "duplicate key value violates unique constraint" in str(e):
                raise HTTPException(status_code=409)
            else:
                raise HTTPException(status_code=400)

        return instance_return(instance)

@router.delete("/instances/{instance_id}", status_code=204)
def delete_instance(instance_id: str):
    with session_scope() as session:
        instance = session.query(Instance).filter(Instance.id == instance_id).one_or_none()
        if not instance:
            raise HTTPException(status_code=404)

        session.delete(instance)
        session.commit()
    return None
