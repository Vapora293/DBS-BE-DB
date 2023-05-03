import uuid

from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing import Optional


# class NoteBaseSchema(BaseModel):
#     id: str | None = None
#     title: str
#     content: str
#     category: str | None = None
#     published: bool = False
#     createdAt: datetime | None = None
#     updatedAt: datetime | None = None
#
#     class Config:
#         orm_mode = True
#         allow_population_by_field_name = True
#         arbitrary_types_allowed = True

class AuthorSchema(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    surname: str

    class Config:
        orm_mode = True


class AuthorUpdateSchema(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None


class Publication(BaseModel):
    id: str | None = None
    title: str
    authors: list[AuthorSchema]
    categories: list[str]
