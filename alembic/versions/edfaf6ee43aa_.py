"""empty message

Revision ID: edfaf6ee43aa
Revises: c039cbfc6f7c
Create Date: 2023-05-06 17:20:15.977780

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'edfaf6ee43aa'
down_revision = 'c039cbfc6f7c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('instance', 'status')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('instance', sa.Column('status', postgresql.ENUM('active', 'inactive', 'expired', name='status_enum'), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
