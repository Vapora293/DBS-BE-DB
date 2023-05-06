from sqlalchemy import Column, TIMESTAMP, func, UUID, String, DATETIME
from enum import Enum

from dbs_assignment.config import engine, Base

from sqlalchemy import Table, ForeignKey
from sqlalchemy.orm import relationship

##TODO: spravit validacie na birthdate, email

publication_authors = Table('publication_authors', Base.metadata,
                            Column('publication_id', UUID, ForeignKey('Publication.id', ondelete='CASCADE'),
                                   primary_key=True),
                            Column('author_id', UUID, ForeignKey('Authors.id', ondelete='CASCADE'), primary_key=True)
                            )

publication_categories = Table('publication_categories', Base.metadata,
                               Column('publication_id', UUID, ForeignKey('Publication.id', ondelete='CASCADE'),
                                      primary_key=True),
                               Column('category_id', UUID, ForeignKey('Category.id', ondelete='CASCADE'),
                                      primary_key=True)
                               )


class Author(Base):
    __tablename__ = 'Authors'
    id = Column(UUID, primary_key=True)
    name = Column(String)
    surname = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class Category(Base):
    __tablename__ = 'Category'
    id = Column(UUID, primary_key=True)
    name = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class Publication(Base):
    __tablename__ = 'Publication'
    id = Column(UUID, primary_key=True)
    title = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    authors = relationship("Author", secondary=publication_authors, backref="authors")
    categories = relationship("Category", secondary=publication_categories, backref="categories")


class Card(Base):
    __tablename__ = 'Card'

    class StatusEnum(Enum):
        ACTIVE = 'active'
        INACTIVE = 'inactive'
        EXPIRED = 'expired'

    id = Column(UUID, primary_key=True)
    user_id = Column(UUID, ForeignKey('User.id'))
    magstripe = Column(String)
    status = Column(String, default=StatusEnum.ACTIVE.value)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class User(Base):
    __tablename__ = 'User'
    id = Column(UUID, primary_key=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String, unique=True)
    birth_date = Column(String)
    personal_identificator = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


Base.metadata.create_all(engine)
