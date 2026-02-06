import asyncio
from logging.config import fileConfig
import sys
import sys
from os.path import dirname, abspath


from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

sys.path.insert(0, dirname(dirname(abspath(__file__))))
from src.config import settings
from src.db.database import Base
from src.features.tasks.model import TasksModel
from src.features.english.model import WordsModel
from sqlalchemy.ext.asyncio import async_engine_from_config
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option("sqlalchemy.url", f"{settings.DB_URL}?async_fallback=True")
# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        # Это поможет избежать проблем с именованием индексов в SQLite
        render_as_batch=True if settings.DB_URL.startswith("sqlite") else False 
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    """Запуск миграций в асинхронном режиме"""
    
    # Создаем асинхронный конфиг
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = settings.DB_URL
    
    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:

        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_offline():
    """Для генерации SQL-скриптов без подключения к БД"""
    url = settings.DB_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())