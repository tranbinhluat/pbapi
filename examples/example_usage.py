"""Example showing basic usage of the Power BI API client."""

from powerbi_api_client import PowerBIAuth, Workspace, Dataset
import pandas as pd


def main() -> None:
    # Load credentials from environment variables
    auth = PowerBIAuth.from_env()

    # List workspaces
    workspace_client = Workspace(auth)
    # Fetch all workspaces with pagination
    workspaces = workspace_client.get_raw(fetch_all=True)
    workspaces_df = pd.DataFrame(workspaces)
    print("Workspaces:")
    print(workspaces_df)

    if not workspaces_df.empty:
        workspace_id = workspaces_df.loc[0, "id"]
        dataset_client = Dataset(auth, workspace_id)
        # Fetch all datasets within the workspace
        datasets = dataset_client.get_raw(fetch_all=True)
        datasets_df = pd.DataFrame(datasets)
        print(f"\nDatasets in workspace {workspace_id}:")
        print(datasets_df)


if __name__ == "__main__":
    main()
