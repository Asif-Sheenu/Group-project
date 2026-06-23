"""add ai review fields

Revision ID: 636d006802c9
Revises: 
Create Date: 2026-06-19 11:55:23.154812

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '636d006802c9'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():

    op.add_column(
        'claims',
        sa.Column(
            'ai_recommendation',
            sa.String(),
            nullable=True
        )
    )

    op.add_column(
        'claims',
        sa.Column(
            'ai_reason',
            sa.Text(),
            nullable=True
        )
    )
    # ### end Alembic commands ###

def downgrade():

    op.drop_column(
        'claims',
        'ai_reason'
    )

    op.drop_column(
        'claims',
        'ai_recommendation'
    )
   
    # ### end Alembic commands ###
