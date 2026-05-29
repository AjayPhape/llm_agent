import logging
from typing import Callable, Dict


from schemas.db import HelperData
from .prompts import categorical_columns

logger = logging.getLogger(__name__)


def get_column_list(helper_data: HelperData) -> Dict[str, str]:
    """
    Retrieve aggregated customer churn data grouped by the given columns.

    Args:
        helper_data (HelperData):
            Configuration object containing:
            - groupColumns: list of database columns used for grouping
            - sortColumns: list of columns used for sorting the result

    Returns:
        A str containing column names.
    """

    if not helper_data:
        return {}

    grouping_columns = helper_data.groupColumns
    sorting_columns = helper_data.sortColumns

    group_column_str = set(grouping_columns).intersection(set(categorical_columns))
    sort_columns_str = set(sorting_columns).intersection(set(categorical_columns))

    # group_column_str = ",".join(group_columns)
    # sort_columns_str = ",".join(sort_columns)

    return {
        "groupColumns": group_column_str,
        "sortColumns": sort_columns_str,
    }


build_tools: list[Callable] = [get_column_list]
