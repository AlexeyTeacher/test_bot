from sqlalchemy import (Column, Integer, String, DateTime,
                        Boolean, ForeignKey, MetaData)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from config import DB_SCHEMA

metadata_obj = MetaData(schema=DB_SCHEMA)
Base = declarative_base(metadata=metadata_obj)
metadata = Base.metadata


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String, comment='Логин как в телеграмме')
    name = Column(String, comment='Имя как в телеграмме')
    is_admin = Column(Boolean)
    created_at = Column(DateTime(timezone=True), comment='Дата и время создания', default='now()')
    updated_at = Column(DateTime(timezone=True), comment='Дата и время последнего обновления')


class ContentType(Base):
    __tablename__ = 'content_types'
    id = Column(Integer, primary_key=True)
    name = Column(String, comment='Название')
    slug = Column(String, comment='Слаг')


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, comment='Название')
    slug = Column(String, comment='Слаг')
    content_type_id = Column(Integer, ForeignKey(ContentType.id, ondelete='CASCADE'))


class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id, ondelete='CASCADE'))
    category_id = Column(Integer, ForeignKey(Category.id, ondelete='CASCADE'))
    name = Column(String, comment='Имя файла для юзера в системе')
    filename = Column(String, comment='Название файла в директории')
    created_at = Column(DateTime(timezone=True), comment='Дата создания',
                        default='now()')

    user = relationship('User')
    category = relationship('Category')


class History(Base):
    __tablename__ = 'histories'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id, ondelete='CASCADE'))
    category_id = Column(Integer, ForeignKey(Category.id, ondelete='CASCADE'))
    name = Column(String, comment='Заголовок')
    description = Column(String, comment='Описание')
    created_at = Column(DateTime(timezone=True), comment='Дата создания', default='now()')

    user = relationship('User')
    category = relationship('Category')
