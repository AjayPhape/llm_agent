import psycopg2
from pydantic.v1 import BaseSettings
from sqlalchemy import URL


class PostgresConfig(BaseSettings):
    host: str = "localhost"
    port: int = 5432
    user: str = "postgres"
    password: str = "postgres"
    database: str = "agent_db"

    db_url = URL.create(
        drivername="postgresql+asyncpg",
        username=user,
        password=password,
        host=host,
        port=port,
        database=database,
    )


DB_ENV = PostgresConfig()
