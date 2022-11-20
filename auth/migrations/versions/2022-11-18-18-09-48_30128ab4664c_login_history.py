"""login_history

Revision ID: 30128ab4664c
Revises: 23e3ffe9984d
Create Date: 2022-11-18 18:09:48.170734

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '30128ab4664c'
down_revision = '23e3ffe9984d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('login_history', sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column('login_history', sa.Column('user_agent', sa.Text(), nullable=True))
    op.add_column('login_history', sa.Column('user_device_type', sa.Text(), nullable=False))
    op.create_unique_constraint('login_history_id_key', 'login_history', ['id'])
    op.create_unique_constraint('login_history_id_user_device_type_key', 'login_history', ['id', 'user_device_type'])
    op.create_foreign_key('login_history_user_id_fkey', 'login_history', 'users', ['user_id'], ['id'])
    op.create_unique_constraint('users_id_key', 'users', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('users_id_key', 'users', type_='unique')
    op.drop_constraint('login_history_user_id_fkey', 'login_history', type_='foreignkey')
    op.drop_constraint('login_history_id_user_device_type_key', 'login_history', type_='unique')
    op.drop_constraint('login_history_id_key', 'login_history', type_='unique')
    op.drop_column('login_history', 'user_device_type')
    op.drop_column('login_history', 'user_agent')
    op.drop_column('login_history', 'user_id')
    # ### end Alembic commands ###
