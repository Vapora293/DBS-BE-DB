"""empty message

Revision ID: 6bd228b58fe6
Revises: 683131723b4d
Create Date: 2023-04-29 17:59:45.639693

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6bd228b58fe6'
down_revision = '683131723b4d'
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
