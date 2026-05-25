import csv
import logging
from contextlib import contextmanager
from io import StringIO
from typing import Any, Dict, List, Optional

import psycopg2
from psycopg2.extras import RealDictCursor

from config.db import DB_ENV

logger = logging.getLogger(__name__)


class PostgresDB:
    def __init__(self) -> None:
        self.connection_params = {
            "host": DB_ENV.host,
            "port": DB_ENV.port,
            "database": DB_ENV.database,
            "user": DB_ENV.user,
            "password": DB_ENV.password,
        }

    @contextmanager
    def get_connection(self):
        """
        Create and manage a PostgreSQL database connection.
        """
        conn = psycopg2.connect(**self.connection_params)
        logger.info("PostgreSQL: connection open")
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
            logger.info("Postgres: connection closed")

    def fetch_query(
        self,
        query: str,
        params: Optional[tuple] = None,
    ) -> List[Dict[str, Any]]:
        """
        Execute a SELECT query and return all rows.

        Args:
            query: SQL query string.
            params: Optional query parameters.

        Returns:
            List of rows as dictionaries.
        """
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params)
                return list(cursor.fetchall())

    def fetch_as_csv(self, query: str) -> str:
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)

                    output = StringIO()
                    writer = csv.writer(output)

                    # header
                    writer.writerow([desc[0] for desc in cursor.description])

                    # rows
                    writer.writerows(cursor.fetchall())

                    return output.getvalue()

        finally:
            conn.close()
