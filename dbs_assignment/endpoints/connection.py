from fastapi import APIRouter
from environs import Env
import psycopg2
from psycopg2.extras import RealDictCursor
import re

# Version of a fulfilled second assessment, first third assessment
env = Env()
env.read_env()
conn = psycopg2.connect(database=env("DATABASE_NAME"), user=env("DATABASE_USER"),
                        password=env("DATABASE_PASSWORD"), host=env("DATABASE_HOST"),
                        port=env("DATABASE_PORT"))
router = APIRouter()


@router.get("/v1/status")
async def status():
    local_cursor = conn.cursor()
    local_cursor.execute('SELECT version();')
    test = local_cursor.fetchall()
    print(test[0][0])
    return {
        'version': test
    }
