"""empty message

Revision ID: 5819059ab6e6
Revises: bf22547dab9a
Create Date: 2023-04-29 18:01:23.090987

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5819059ab6e6'
down_revision = 'bf22547dab9a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Authors', sa.Column('updatedAt', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Authors', 'updatedAt')
    # ### end Alembic commands ###
