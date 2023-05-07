from uuid import UUID, uuid4
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, Field, validator


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

    @validator('name')
    def validate_name(cls, name):
        if name is not None and isinstance(int(name), int):
            raise ValueError()
        return name
    class Config:
        orm_mode = True


class CategoryUpdateSchema(BaseModel):
    name: Optional[str] = None
    @validator('name', allow_reuse=True)
    def validate_name(cls, name):
        if name is not None and isinstance(int(name), int):
            raise ValueError()
        return name


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

class ReservationSchema(BaseModel):
    id: UUID
    user_id: UUID
    publication_id: UUID

class ReservationOut(BaseModel):
    id: UUID
    user_id: UUID
    publication_id: UUID
    created_at: datetime

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


class RentalSchema(BaseModel):
    id: UUID
    user_id: UUID
    publication_id: UUID
    duration: int


class RentalOut(BaseModel):
    id: UUID
    user_id: UUID
    publication_instance_id: UUID
    duration: int
    start_date: datetime
    end_date: datetime
    status: str

    class Config:
        orm_mode = True


class RentalUpdateSchema(BaseModel):
    duration: int


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
    personal_identificator: str
    rentals: Optional[List[RentalOut]] = None
    reservations: Optional[List[ReservationOut]] = None
    created_at: datetime
    updated_at: datetime


class InstanceSchema(BaseModel):
    id: UUID
    type: str
    publisher: str
    year: int
    status: Optional[str]
    publication_id: UUID


class InstanceUpdateSchema(BaseModel):
    type: Optional[str]
    publisher: Optional[str]
    year: Optional[int]
    status: Optional[str]
    publication_id: Optional[UUID]


class InstanceOut(BaseModel):
    id: UUID
    type: str
    publisher: str
    year: int
    status: str
    publication_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
