from environs import Env
from pydantic import BaseSettings
from dotenv import find_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class MySettings(BaseSettings):
    class Config:
        env_file = find_dotenv()
        case_sensitive = True

    DATABASE_HOST: str
    DATABASE_PORT: str
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str


conf = MySettings()

env = Env()
env.read_env()

DATABASE_URI = 'postgresql+psycopg2://' + env("DATABASE_USER") + ':' + env("DATABASE_PASSWORD") + '@' + env(
    "DATABASE_HOST") + ":" + env("DATABASE_PORT") + '/' + env("DATABASE_NAME")
engine = create_engine(DATABASE_URI, future=True)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, future=True
)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

engine.connect()
