# Module `agents_monitor_bills.parsers.openstates_bill_parser`

## Functions

### `gql(request_string: 'str | Source') -> 'DocumentNode'`

Given a string containing a GraphQL request, parse it into a Document.

:param request_string: the GraphQL request as a String
:type request_string: str | Source
:return: a Document which can be later executed or subscribed by a
    :class:`Client <gql.client.Client>`, by an
    :class:`async session <gql.client.AsyncClientSession>` or by a
    :class:`sync session <gql.client.SyncClientSession>`

:raises GraphQLError: if a syntax error is encountered.

### `run(storage_path, config, api_key)`

Query OpenStates for all bills and return counts by jurisdiction.

Args:
    storage_path (Path or str): Path where output can be written (not used here, but kept for symmetry).
    config (dict): Configuration dictionary with at least 'openstates_graphql_url'.
    api_key (str): API key for authenticating the request.

Returns:
    list of dict: [{'jurisdiction': 'X', 'bill_count': N}, ...] or error message string
