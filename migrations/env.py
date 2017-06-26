from __future__ import with_statement
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
import logging

import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from flask import current_app

from application import create_app, db


from application import User, Project, Branch, Thread, Comment, Likes, User_Tag, File_Tag, Named_Tag, Custom_Tag, Free_Tag, limiter, mail

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

app = create_app(dict(
    TESTING=True,  # Propagate exceptions
    LOGIN_DISABLED=False,  # Enable @register_required
    MAIL_SUPPRESS_SEND=True,  # Disable Flask-Mail send
    SQLALCHEMY_DATABASE_URI=('mysql://gutosurrex:8yutjgusuii3hf9kd9d99'
                             '@localhost/bookcloud'),
    WTF_CSRF_ENABLED=False,  # Disable CSRF form validation
    BOOKCLOUD_URL_PREFIX = '',
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    #USER_AFTER_LOGIN_ENDPOINT                = 'user.login'
    # v0.5.3 and up
))
app.app_context()

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
#from flask import current_app
#config.set_main_option('sqlalchemy.url',
#                       current_app.config.get('SQLALCHEMY_DATABASE_URI'))
#target_metadata = current_app.extensions['migrate'].db.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    # this callback is used to prevent an auto-migration from being generated
    # when there are no changes to the schema
    # reference: http://alembic.readthedocs.org/en/latest/cookbook.html

    alembic_config = config.get_section(config.config_ini_section)
    alembic_config['sqlalchemy.url'] = app.config['SQLALCHEMY_DATABASE_URI']

    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info('No changes in schema detected.')

    engine = engine_from_config(alembic_config,
                                prefix='sqlalchemy.',
                                poolclass=pool.NullPool)

    connection = engine.connect()
    context.configure(connection=connection,
                      target_metadata=db.metadata,
                      compare_type=True,
                      process_revision_directives=process_revision_directives)

    try:
        with context.begin_transaction():
            context.run_migrations()
    finally:
        connection.close()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
