"""empty message

Revision ID: 35877c2294d9
Revises: b2744bbd5737
Create Date: 2023-05-06 17:53:40.978790

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35877c2294d9'
down_revision = 'b2744bbd5737'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'Category', ['name'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Category', type_='unique')
    # ### end Alembic commands ###
