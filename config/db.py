from pydantic.v1 import BaseSettings


class PostgresConfig(BaseSettings):
    host: str = "localhost"
    port: int = 5432
    user: str = "postgres"
    password: str = "postgres"
    database: str = "zinkworks"


DB_ENV = PostgresConfig()
