"""Example showing basic usage of the Power BI API client."""

from powerbi_api_client import PowerBIAuth, Workspace, Dataset


def main() -> None:
    # Load credentials from environment variables
    auth = PowerBIAuth.from_env()

    # List workspaces
    workspace_client = Workspace(auth)
    workspaces_df = workspace_client.to_dataframe(fetch_all=True)
    print("Workspaces:")
    print(workspaces_df)

    if not workspaces_df.empty:
        workspace_id = workspaces_df.loc[0, "id"]
        dataset_client = Dataset(auth, workspace_id)
        datasets_df = dataset_client.to_dataframe(fetch_all=True)
        print(f"\nDatasets in workspace {workspace_id}:")
        print(datasets_df)


if __name__ == "__main__":
    main()
