from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing import Optional


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


class Publication(BaseModel):
    id: str | None = None
    title: str
    authors: list[AuthorSchema]
    categories: list[str]
