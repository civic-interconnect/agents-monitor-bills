"""
parsers/openstates_bill_parser.py

Queries OpenStates GraphQL for basic bill counts.
"""

import asyncio
import pandas as pd
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import TransportServerError, TransportQueryError, TransportProtocolError
from loguru import logger

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

async def fetch_bills(api_key, config):
    url = config["openstates_graphql_url"]
    headers = {"Authorization": f"Bearer {api_key}"}

    transport = AIOHTTPTransport(url=url, headers=headers, ssl=True)
    client = Client(transport=transport, fetch_schema_from_transport=False)

    bills = []
    after = None

    while True:
        variables = {"first": 100, "after": after}
        response = await client.execute_async(BILL_QUERY, variable_values=variables)
        edges = response["bills"]["edges"]
        for edge in edges:
            bill = edge["node"]
            bills.append({
                "id": bill["id"],
                "jurisdiction": bill["jurisdiction"]["name"]
            })
        page = response["bills"]["pageInfo"]
        if not page["hasNextPage"]:
            break
        after = page["endCursor"]

    logger.info(f"Fetched {len(bills)} bills total")
    return pd.DataFrame(bills)

def run(storage_path, config, api_key):
    logger.info("Pulling OpenStates bill summary...")

    try:
        df = asyncio.run(fetch_bills(api_key, config))

        grouped = df.groupby("jurisdiction").size().reset_index(name="bill_count")
        summary = grouped.to_dict(orient="records")
        logger.info(f"Summary: {summary}")
        return summary

    except TransportServerError as e:
        if "403" in str(e):
            logger.warning("OpenStates bill access not yet enabled (received 403 Forbidden).")
            return "Bill data access not yet granted"
        else:
            logger.error(f"Server error: {e}")
            raise

    except TransportQueryError as e:
        logger.error(f"GraphQL query error: {e}")
        raise

    except TransportProtocolError as e:
        logger.error(f"Transport protocol error: {e}")
        raise

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise
