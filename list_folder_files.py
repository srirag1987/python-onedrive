import os
import httpx
from dotenv import load_dotenv
from ms_graph import get_access_token, MS_GRAPH_BASE_URL


# -------------------------------------------------------
#  Get SharePoint Site ID
# -------------------------------------------------------

def get_site_id(headers, site_hostname, site_path):
    url = f"{MS_GRAPH_BASE_URL}/sites/{site_hostname}:{site_path}"
    response = httpx.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["id"]


# -------------------------------------------------------
#  Get ALL Drives in the Site, then select the CAD drive
# -------------------------------------------------------

def get_cad_drive_id(headers, site_id):
    url = f"{MS_GRAPH_BASE_URL}/sites/{site_id}/drives"
    response = httpx.get(url, headers=headers)
    response.raise_for_status()

    drives = response.json().get("value", [])

    for d in drives:
        if d.get("name") == "CAD":
            return d["id"]

    raise Exception("CAD document library not found in /drives!")


# -------------------------------------------------------
#  List all children in the root of the CAD drive
# -------------------------------------------------------

def list_drive_root(headers, site_id, drive_id):
    url = f"{MS_GRAPH_BASE_URL}/sites/{site_id}/drives/{drive_id}/root/children"
    response = httpx.get(url, headers=headers)
    response.raise_for_status()
    return response.json().get("value", [])


# -------------------------------------------------------
#  Pretty print output (folders & files)
# -------------------------------------------------------

def print_items(items):
    if not items:
        print("No items found in CAD document library.\n")
        return

    for item in items:
        if "folder" in item:
            print(f"[FOLDER] {item['name']} | ChildCount: {item['folder']['childCount']}")
        else:
            size_kb = item["size"] / 1024
            print(f"[FILE]   {item['name']} | {size_kb:.2f} KB")

    print("-" * 60)


# -------------------------------------------------------
#  MAIN
# -------------------------------------------------------

def main():
    load_dotenv()

    application_id = os.getenv("APPLICATION_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    site_hostname = os.getenv("SITE_HOSTNAME")
    site_path = os.getenv("SITE_PATH")

    scopes = ["https://graph.microsoft.com/.default"]

    try:
        print("Getting access token...")
        access_token = get_access_token(application_id, client_secret, scopes)

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }

        print("\nResolving SharePoint Site...")
        site_id = get_site_id(headers, site_hostname, site_path)
        print(f"Site ID: {site_id}\n")

        print("Retrieving CAD Document Library (Drive) ID...")
        cad_drive_id = get_cad_drive_id(headers, site_id)
        print(f"CAD Drive ID: {cad_drive_id}\n")

        print("Listing items in CAD document library root...\n")
        items = list_drive_root(headers, site_id, cad_drive_id)
        print_items(items)

    except Exception as e:
        print("\nERROR:", e)


if __name__ == "__main__":
    main()
