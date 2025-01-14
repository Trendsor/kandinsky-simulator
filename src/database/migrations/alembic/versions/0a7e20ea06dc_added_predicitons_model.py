"""added predicitons model

Revision ID: 0a7e20ea06dc
Revises: 6910163a9cb6
Create Date: 2024-12-16 19:07:18.640868

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0a7e20ea06dc'
down_revision: Union[str, None] = '6910163a9cb6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stock_data_prediction',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('symbol', sa.String(length=10), nullable=False),
    sa.Column('price', sa.DECIMAL(), nullable=False),
    sa.Column('size', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.TIMESTAMP(), nullable=False),
    sa.Column('rolling_mean_200', sa.DECIMAL(), nullable=True),
    sa.Column('rolling_std_200', sa.DECIMAL(), nullable=True),
    sa.Column('target', sa.Integer(), nullable=True),
    sa.Column('predictions', sa.DECIMAL(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stock_data_prediction')
    # ### end Alembic commands ###
