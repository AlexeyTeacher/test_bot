import os

from alembic.script import ScriptDirectory
from alembic import command
from alembic.config import Config
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.sql.ddl import CreateSchema

from config import logger, DB_SCHEMA
from db import ENGINE


def upgrade_revisions(engine, revision=''):
    logger.info(f'Upgrade Alembic with {engine}')
    try:
        engine.execute(CreateSchema(DB_SCHEMA))
    except ProgrammingError:
        logger.error('Schema is created')
    root_dir = os.path.dirname(os.path.realpath(__file__))
    config_file = os.path.join(root_dir, "alembic.ini")
    migrations_dir = os.path.join(root_dir, "alembic")
    # Pass engine to alembic env.py file
    config_alembic = Config(file_=config_file, attributes={'engine': engine})
    config_alembic.set_main_option("script_location", migrations_dir)
    # Block for manual migrations
    if revision:
        command.upgrade(config_alembic, revision=revision)
        return
    # Collect revisions
    script_alembic = ScriptDirectory.from_config(config_alembic)
    base = script_alembic.get_base()
    head = script_alembic.get_current_head()
    revisions = [
        {'id': _.revision, 'name': _.doc}
        for _ in script_alembic.iterate_revisions(lower=base, upper=head)]
    revisions.append({'id': base, 'name': 'init'})
    logger.info(f'Alembic revisions: {revisions}')
    # Execute revisions
    try:
        for r in revisions[::-1]:
            command.upgrade(config_alembic, revision=r['id'])
    except ProgrammingError as e:
        logger.error(e)


if __name__ == '__main__':
    upgrade_revisions(ENGINE)
