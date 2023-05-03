from sqlalchemy import Column, TIMESTAMP, func, VARCHAR, UUID
from dbs_assignment.config import engine, Base


class BaseModel(Base):
    __tablename__ = 'Base'
    id = Column(VARCHAR, primary_key=True)
    createdAt = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updatedAt = Column(TIMESTAMP(timezone=True), server_default=func.now())


class Author(Base):
    __tablename__ = 'Authors'
    id = Column(UUID, primary_key=True)
    name = Column(VARCHAR)
    surname = Column(VARCHAR)
    createdAt = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updatedAt = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class Category(Base):
    __tablename__= 'Category'
    id = Column(UUID, primary_key=True)
    name = Column(VARCHAR)
    createdAt = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updatedAt = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

Base.metadata.create_all(engine)

# class Category(BaseModel):
#     id = models.UUIDField(
#         primary_key=True,
#         default=uuid.uuid4,
#         editable=False
#     )
#     name = models.CharField(max_length=255)
#
#
# class Publication(BaseModel):
#     id = models.UUIDField(
#         primary_key=True,
#         default=uuid.uuid4,
#         editable=False
#     )
#     title = models.CharField(max_length=255)
#     authors = models.ManyToManyField(Author, db_table='author_publication')
#     categories = models.ManyToManyField(Category, db_table='category_publication')
#
#     def __str__(self) -> str:
#         return self.name
