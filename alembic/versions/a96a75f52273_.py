"""empty message

Revision ID: a96a75f52273
Revises: acb6f4aa279e
Create Date: 2023-04-29 16:22:28.809851

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a96a75f52273'
down_revision = 'acb6f4aa279e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Base')
    op.drop_table('Authors')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Authors',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('surname', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('createdAt', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.Column('updatedAt', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='Authors_pkey')
    )
    op.create_table('Base',
    sa.Column('id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('createdAt', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.Column('updatedAt', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='Base_pkey')
    )
    # ### end Alembic commands ###
