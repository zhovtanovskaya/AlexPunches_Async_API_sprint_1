"""first

Revision ID: ac8e4e98a1b7
Revises: 
Create Date: 2022-11-21 12:27:02.096099

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ac8e4e98a1b7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id')
    )
    op.create_table('login_history',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('date_login', sa.DateTime(), nullable=True),
    sa.Column('user_agent', sa.Text(), nullable=True),
    sa.Column('user_device_type', sa.Text(), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id', 'user_device_type'),
    sa.UniqueConstraint('id', 'user_device_type'),
    postgresql_partition_by='LIST (user_device_type)'
    )
    op.create_table('roles_users',
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    op.create_table('social_account',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('social_id', sa.Text(), nullable=False),
    sa.Column('social_name', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('social_id', 'social_name', name='social_pk')
    )
    op.create_table('login_history_mobile',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('date_login', sa.DateTime(), nullable=True),
    sa.Column('user_agent', sa.Text(), nullable=True),
    sa.Column('user_device_type', sa.Text(), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id', 'user_device_type')
    )
    op.create_table('login_history_smart',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('date_login', sa.DateTime(), nullable=True),
    sa.Column('user_agent', sa.Text(), nullable=True),
    sa.Column('user_device_type', sa.Text(), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id', 'user_device_type')
    )
    op.create_table('login_history_web',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('date_login', sa.DateTime(), nullable=True),
    sa.Column('user_agent', sa.Text(), nullable=True),
    sa.Column('user_device_type', sa.Text(), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id', 'user_device_type')
    )
    # ### end Alembic commands ###


    from models.patition_login_history import (
        PARTITION_TABLES_REGISTRY,
        create_table_login_history_partition_ddl
    )    
    for table_class, device_type in PARTITION_TABLES_REGISTRY:
        ddl = create_table_login_history_partition_ddl(table_class.__table__, device_type)
        ddl(target=None, bind=op.get_bind())


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('login_history_web')
    op.drop_table('login_history_smart')
    op.drop_table('login_history_mobile')
    op.drop_table('social_account')
    op.drop_table('roles_users')
    op.drop_table('login_history')
    op.drop_table('users')
    op.drop_table('roles')
    # ### end Alembic commands ###