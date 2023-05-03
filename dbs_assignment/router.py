from fastapi import APIRouter

import dbs_assignment.models
from dbs_assignment.config import engine
from dbs_assignment.endpoints import connection

router = APIRouter()
router.include_router(connection.router, tags=["hello"])

dbs_assignment.models.Base.metadata.create_all(bind=engine)
