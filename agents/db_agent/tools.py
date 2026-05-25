import logging
from typing import Callable, Dict, List

from .prompts import categorical_columns
from .schemas import Data
from .utils import PostgresDB

logger = logging.getLogger(__name__)


def get_data(grouping_columns: list) -> str:
    """
    Retrieve aggregated customer churn data grouped by the given columns.

    Args:
        grouping_columns: List of database column names used for grouping.

    Returns:
        A list of dictionaries containing grouped records and their counts.
    """

    if not grouping_columns:
        return ""

    group_columns = set(grouping_columns).intersection(set(categorical_columns))

    group_column_str = ",".join(group_columns)

    query = f"""
    SELECT
        {group_column_str},
        COUNT(*) AS total_count
    FROM
        customer_churn cc
    GROUP BY
        {group_column_str}
    """

    try:
        return PostgresDB().fetch_as_csv(query)
    except Exception as exc:
        logger.exception("Failed to fetch grouped customer churn data: %s", exc)
        return ""


build_tools: list[Callable] = [get_data]
