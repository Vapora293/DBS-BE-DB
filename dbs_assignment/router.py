from fastapi import APIRouter

import dbs_assignment.models
from dbs_assignment.config import engine
from dbs_assignment.endpoints import connection, authors, categories, publications

router = APIRouter()
router.include_router(connection.router)
router.include_router(authors.router)
router.include_router(categories.router)
router.include_router(publications.router)
dbs_assignment.models.Base.metadata.create_all(bind=engine)
