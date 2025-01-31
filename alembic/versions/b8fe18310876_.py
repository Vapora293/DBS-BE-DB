"""empty message

Revision ID: b8fe18310876
Revises: edfaf6ee43aa
Create Date: 2023-05-06 17:20:39.696108

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b8fe18310876'
down_revision = 'edfaf6ee43aa'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('instance', sa.Column('status', sa.Enum('available', 'reserved', name='statusInstance_enum'), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('instance', 'status')
    # ### end Alembic commands ###
