from logging.config import fileConfig
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection
from alembic import context
from config.config import settings
from db.base import Base  # Убедитесь, что это импортируется правильно
from db.models.memes import Memes  # Импортируйте вашу модель, чтобы Alembic знал о ней

# Настройка URL базы данных
url = settings.DATABASE_URL

# Конфигурация Alembic
config = context.config

# Устанавливаем логгеры из файла конфигурации
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Мета-данные для ваших моделей
target_metadata = Base.metadata

def run_migrations_offline():
    """Запуск миграций в оффлайн-режиме."""
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    """Запуск миграций в онлайн-режиме."""
    connectable = create_async_engine(url, future=True, echo=True)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def do_run_migrations(connection: AsyncConnection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        render_as_batch=True  # Если используете режим batch
    )

    with context.begin_transaction():
        context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    try:
        asyncio.run(run_migrations_online())
    except Exception as e:
        print(f"Error during migration: {e}")
        raise
