"""Initial migration

Revision ID: 4cd911e0e695
Revises: 
Create Date: 2024-12-05 08:05:54.428425

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4cd911e0e695'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stock_data_processed',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('symbol', sa.String(length=10), nullable=False),
    sa.Column('price', sa.DECIMAL(), nullable=False),
    sa.Column('size', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.TIMESTAMP(), nullable=False),
    sa.Column('rolling_mean_200', sa.DECIMAL(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('stock_data_raw',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('symbol', sa.String(length=10), nullable=False),
    sa.Column('price', sa.DECIMAL(), nullable=False),
    sa.Column('size', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.TIMESTAMP(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stock_data_raw')
    op.drop_table('stock_data_processed')
    # ### end Alembic commands ###
