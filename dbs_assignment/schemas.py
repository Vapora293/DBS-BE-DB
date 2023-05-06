from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing import Optional, List

from datetime import datetime


class AuthorSchema(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    surname: str

    class Config:
        orm_mode = True


class AuthorUpdateSchema(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None


class CategorySchema(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str

    class Config:
        orm_mode = True


class CategoryUpdateSchema(BaseModel):
    name: Optional[str] = None


class AuthorCreate(BaseModel):
    name: str
    surname: str


class PublicationSchema(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    authors: List[AuthorCreate]
    categories: List[str]


class PublicationOut(BaseModel):
    id: UUID
    title: str
    authors: List[dict]
    categories: List[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
