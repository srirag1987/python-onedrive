import os
import httpx
from dotenv import load_dotenv
from ms_graph import get_access_token, MS_GRAPH_BASE_URL


def get_site_id(headers, site_hostname, site_path):
    url = f"{MS_GRAPH_BASE_URL}/sites/{site_hostname}:{site_path}"
    response = httpx.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["id"]


def list_drive_root(headers, site_id):
    url = f"{MS_GRAPH_BASE_URL}/sites/{site_id}/drive/root/children"
    response = httpx.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["value"]


def print_items(items):
    for item in items:
        if "folder" in item:
            print(f"[FOLDER] {item['name']}  | Items: {item['folder']['childCount']}")
        else:
            size_kb = item["size"] / 1024
            print(f"[FILE]   {item['name']}  | {size_kb:.2f} KB")
    print("-" * 60)


def main():
    load_dotenv()

    application_id = os.getenv("APPLICATION_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    site_hostname = os.getenv("SITE_HOSTNAME")
    site_path = os.getenv("SITE_PATH")

    scopes = ["https://graph.microsoft.com/.default"]

    try:
        access_token = get_access_token(application_id, client_secret, scopes)

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }

        print("Resolving SharePoint site...")
        site_id = get_site_id(headers, site_hostname, site_path)
        print(f"Site ID: {site_id}\n")

        print("Listing contents of CAD document library (drive root):\n")
        items = list_drive_root(headers, site_id)
        print_items(items)

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
