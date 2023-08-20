"""add settings info

Revision ID: a66363c4f3bd
Revises: 83fe63943e2e
Create Date: 2023-08-18 22:36:24.145260

"""
from alembic import op
import sqlalchemy as sa
from config import DB_SCHEMA, OWNER_NAME, OWNER_LOGIN
from db import ENGINE



# revision identifiers, used by Alembic.
revision = 'a66363c4f3bd'
down_revision = '83fe63943e2e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()

    conn.execute(f"""INSERT INTO {DB_SCHEMA}.users (login, name, is_admin) 
                     VALUES ('{OWNER_LOGIN}', '{OWNER_NAME}', true);
                     """)

    conn.execute(f"""INSERT INTO {DB_SCHEMA}.content_types (id, slug, name) 
                     VALUES (1, 'image', 'Изображение'),
                            (2, 'voice', 'Голосовое сообщение'),
                            (3, 'text', 'Текстовое сообщение');
                         """)
    conn.execute(f"""INSERT INTO {DB_SCHEMA}.categories (id, slug, name, content_type_id) 
                     VALUES (1, 'last_selfie', '🤳 Последнее селфи', 1),
                            (2, 'school_photo', '🎒 Фото из старшей школы', 1),
                            (3, 'story', '❤️ Главное увлечение', 3),
                            (4, 'gpt', '🤖 «Объясняю своей бабушке», что такое GPT', 2),
                            (5, 'bases', '🐘 Разница между SQL и NoSQL', 2),
                            (6, 'first_love', '❤️‍🔥 Первая любовь', 2);
                             """)


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(f"""TRUNCATE {DB_SCHEMA}.users, {DB_SCHEMA}.content_types, {DB_SCHEMA}.categories; """)
