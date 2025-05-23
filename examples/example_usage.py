"""Example showing basic usage of the Power BI API client."""

import argparse
import pandas as pd

from powerbi_api_client import Dashboard, DataModel, Dataset, PowerBIAuth, Workspace


def parse_args() -> argparse.Namespace:
    """Return command line arguments for the example script."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--workspace-id",
        help="Fetch datasets for the given workspace id. If omitted, the first workspace is used.",
    )
    parser.add_argument(
        "--dataset-id",
        help=(
            "Show tables for the given dataset id. If omitted, the first dataset "
            "in the workspace is used."
        ),
    )
    parser.add_argument(
        "--show-dashboards",
        action="store_true",
        help="Display dashboards for the selected workspace.",
    )
    return parser.parse_args()


def main() -> None:
    """Run the example using optional command line arguments."""
    args = parse_args()

    # Load credentials from environment variables
    auth = PowerBIAuth.from_env()

    # List workspaces
    workspace_client = Workspace(auth)
    workspaces = workspace_client.get_raw(fetch_all=True)
    workspaces_df = pd.DataFrame(workspaces)
    print("Workspaces:")
    print(workspaces_df)

    if not workspaces_df.empty:
        workspace_id = args.workspace_id or workspaces_df.loc[0, "id"]
        dataset_client = Dataset(auth, workspace_id)
        datasets = dataset_client.get_raw(fetch_all=True)
        datasets_df = pd.DataFrame(datasets)
        print(f"\nDatasets in workspace {workspace_id}:")
        print(datasets_df)

        if datasets_df.empty:
            return

        dataset_id = args.dataset_id or datasets_df.loc[0, "id"]
        model_client = DataModel(auth, workspace_id, dataset_id)
        tables = model_client.get_raw(fetch_all=True)
        tables_df = pd.DataFrame(tables)
        print(f"\nTables in dataset {dataset_id}:")
        print(tables_df)

        if args.show_dashboards:
            dashboard_client = Dashboard(auth, workspace_id)
            dashboards = dashboard_client.get_raw(fetch_all=True)
            dashboards_df = pd.DataFrame(dashboards)
            print(f"\nDashboards in workspace {workspace_id}:")
            print(dashboards_df)


if __name__ == "__main__":
    main()
