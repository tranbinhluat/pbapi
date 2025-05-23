# Power BI API Client

A lightweight Python client for interacting with the Power BI REST API. The
library provides simple, object-oriented helpers to authenticate, list
workspaces, fetch datasets and inspect data models.

## Installation

Create a virtual environment and install the dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Authentication details are read from environment variables. Create a `.env`
file or export the following variables in your environment:

```
POWERBI_TENANT_ID=<your-tenant-id>
POWERBI_CLIENT_ID=<your-client-id>
POWERBI_CLIENT_SECRET=<your-client-secret>
```

The client authenticates using an Azure AD service principal via the
`msal` library.

## Example Usage

Run the example script to list workspaces and datasets:

```bash
python examples/example_usage.py
```

You can specify a workspace to list datasets from using the ``--workspace-id``
flag. You can also print tables for a specific dataset using ``--dataset-id``
and display dashboards with ``--show-dashboards``:

```bash
python examples/example_usage.py --workspace-id YOUR_WORKSPACE_ID \
    --dataset-id YOUR_DATASET_ID --show-dashboards
```

This will output a table of your Power BI workspaces and datasets using
`pandas` DataFrames.

All `get_raw` methods accept a `fetch_all` flag. When set to `True`, the
client automatically handles `$top`/`$skip` pagination and returns all
records.

## Extending

The codebase is structured to be easily extended for additional Power BI
endpoints. Each entity class contains two core methods:

* `get_raw` - fetch raw JSON data from the API.
* `to_dataframe` - return the data as a `pandas` DataFrame for analysis.

Additional helpers and endpoints can be implemented following the same
pattern.
