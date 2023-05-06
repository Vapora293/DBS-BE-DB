from uuid import UUID, uuid4
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr


class AuthorSchema(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    surname: str

    class Config:
        orm_mode = True


class AuthorUpdateSchema(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None


class AuthorCreate(BaseModel):
    name: str
    surname: str


class CategorySchema(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str

    class Config:
        orm_mode = True


class CategoryUpdateSchema(BaseModel):
    name: Optional[str] = None


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


class CardSchema(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID = Field(default_factory=uuid4)
    magstripe: str
    status: str


class CardOut(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID = Field(default_factory=uuid4)
    magstripe: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class CardUpdateSchema(BaseModel):
    status: Optional[str]
    user_id: Optional[str]


class UserSchema(BaseModel):
    id: UUID
    name: str
    surname: str
    email: str
    birth_date: date
    personal_identificator: str

class UserUpdateSchema(BaseModel):
    name: Optional[str]
    surname: Optional[str]
    email: Optional[str]
    birth_date: Optional[date]
    personal_identificator: Optional[str]


class UserOut(BaseModel):
    id: UUID
    name: str
    surname: str
    email: str
    birth_date: date
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
