"""init

Revision ID: 83fe63943e2e
Revises: 
Create Date: 2023-08-18 22:16:05.625754

"""
from alembic import op
import sqlalchemy as sa
from config import DB_SCHEMA
from db import ENGINE

# revision identifiers, used by Alembic.
revision = '83fe63943e2e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('content_types',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=True, comment='Название'),
                    sa.Column('slug', sa.String(), nullable=True, comment='Слаг'),
                    sa.PrimaryKeyConstraint('id'),
                    schema='practicum'
                    )
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('login', sa.String(), nullable=True, comment='Логин как в телеграмме'),
                    sa.Column('name', sa.String(), nullable=True, comment='Имя как в телеграмме'),
                    sa.Column('is_admin', sa.Boolean(), nullable=True),
                    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True, comment='Дата и время создания'),
                    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True,
                              comment='Дата и время последнего обновления'),
                    sa.PrimaryKeyConstraint('id'),
                    schema='practicum'
                    )
    op.create_table('categories',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=True, comment='Название'),
                    sa.Column('slug', sa.String(), nullable=True, comment='Слаг'),
                    sa.Column('content_type_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['content_type_id'], ['practicum.content_types.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id'),
                    schema='practicum'
                    )
    op.create_table('documents',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('category_id', sa.Integer(), nullable=True),
                    sa.Column('name', sa.String(), nullable=True, comment='Имя файла для юзера в системе'),
                    sa.Column('filename', sa.String(), nullable=True, comment='Название файла в директории'),
                    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True, comment='Дата создания'),
                    sa.ForeignKeyConstraint(['category_id'], ['practicum.categories.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['user_id'], ['practicum.users.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id'),
                    schema='practicum'
                    )
    op.create_table('histories',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('category_id', sa.Integer(), nullable=True),
                    sa.Column('name', sa.String(), nullable=True, comment='Заголовок'),
                    sa.Column('description', sa.String(), nullable=True, comment='Описание'),
                    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True, comment='Дата создания'),
                    sa.ForeignKeyConstraint(['category_id'], ['practicum.categories.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['user_id'], ['practicum.users.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id'),
                    schema='practicum'
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('histories', schema='practicum')
    op.drop_table('documents', schema='practicum')
    op.drop_table('categories', schema='practicum')
    op.drop_table('users', schema='practicum')
    op.drop_table('content_types', schema='practicum')
    # ### end Alembic commands ###
