import logging
from pydoc import Helper
from typing import Callable, Dict, List

from google.adk.tools.toolbox_toolset import ToolboxToolset
from tabulate import tabulate

from config.llm import MCP_TOOLBOX_URL, MCP_TOOLSET
from db_agent.utils import PostgresDB
from schemas.db import HelperData

logger = logging.getLogger(__name__)


def get_summarized_data(helper_data: HelperData):
    """
    Retrieve aggregated customer churn statistics grouped by one or more columns.

    The result includes:
    - selected grouping columns
    - total_count: number of matching records per group

    Args:
        helper_data (object): Object containing information about groupColumns, sortColumns

    Returns:
        str:
            A GitHub-formatted markdown table containing aggregated counts.

    """

    grouped_columns = ','.join(helper_data.groupColumns)
    sort_columns = ','.join(helper_data.sortColumns)

    query = f"""
    SELECT
        {grouped_columns},
        COUNT(*) AS total_count
    FROM
        customer_churn cc
    GROUP BY
    GROUPING SETS 
        (({grouped_columns}), ())
    ORDER BY
        ({sort_columns})
    """

    try:
        data = PostgresDB().fetch_query(query)
        return tabulate(data, headers="keys", tablefmt="github")
    except Exception as exc:
        logger.exception("Failed to fetch grouped customer churn data: %s", exc)
        return ""


toolset = ToolboxToolset(
    server_url=MCP_TOOLBOX_URL,
    toolset_name=MCP_TOOLSET
)

build_tools: list = [toolset]
