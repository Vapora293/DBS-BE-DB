from fastapi import APIRouter

import dbs_assignment.models
from dbs_assignment.config import engine
from dbs_assignment.endpoints import connection, authors, categories, publications, cards, users, instance

router = APIRouter()
router.include_router(connection.router)
router.include_router(authors.router)
router.include_router(categories.router)
router.include_router(publications.router)
router.include_router(cards.router)
router.include_router(users.router)
router.include_router(instance.router)
dbs_assignment.models.Base.metadata.create_all(bind=engine)
