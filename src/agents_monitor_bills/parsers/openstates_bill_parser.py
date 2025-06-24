"""
parsers/openstates_bill_parser.py

Queries OpenStates GraphQL for basic bill counts.

MIT License — Civic Interconnect
"""

import pandas as pd
from civic_lib_core import api_utils, error_utils, log_utils
from gql import gql

logger = log_utils.logger

BILL_QUERY = gql("""
query BillSummary($first: Int, $after: String) {
  bills(first: $first, after: $after) {
    pageInfo {
      hasNextPage
      endCursor
    }
    edges {
      node {
        jurisdiction { id name }
        id
      }
    }
  }
}
""")


def run(storage_path, config, api_key):
    """
    Query OpenStates for all bills and return counts by jurisdiction.

    Args:
        storage_path (Path or str): Path where output can be written (not used here, but kept for symmetry).
        config (dict): Configuration dictionary with at least 'openstates_graphql_url'.
        api_key (str): API key for authenticating the request.

    Returns:
        list of dict: [{'jurisdiction': 'X', 'bill_count': N}, ...] or error message string
    """
    logger.info("Starting OpenStates bill monitoring...")

    try:
        response = api_utils.paged_query(
            url=config["openstates_graphql_url"],
            api_key=api_key,
            query=BILL_QUERY,
            data_path=["bills", "edges"],
        )

        bills = [
            {
                "id": edge["node"]["id"],
                "jurisdiction": edge["node"]["jurisdiction"]["name"],
            }
            for edge in response
        ]

        df = pd.DataFrame(bills)
        summary_df = df.groupby("jurisdiction").size().reset_index(name="bill_count")
        summary = summary_df.to_dict(orient="records")

        logger.info(f"Bill summary completed with {len(summary)} jurisdictions.")
        return summary

    except Exception as e:
        return error_utils.handle_transport_errors(e, resource_name="OpenStates Bill Monitor")
