"""Add technical_objective to bossdefinition

Revision ID: add_boss_technical_objective
Revises: 
Create Date: 2025-12-04

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_boss_technical_objective'
down_revision = None  # Update this to your latest migration
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add technical_objective column to bossdefinition table
    op.add_column(
        'bossdefinition',
        sa.Column('technical_objective', sa.String(), nullable=False, server_default='')
    )
    
    # Remove server default after column is added
    op.alter_column('bossdefinition', 'technical_objective', server_default=None)


def downgrade() -> None:
    # Remove technical_objective column
    op.drop_column('bossdefinition', 'technical_objective')
