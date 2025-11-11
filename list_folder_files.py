import os
import httpx
from dotenv import load_dotenv
from ms_graph import get_access_token, MS_GRAPH_BASE_URL

def list_root_folder(headers):
    url = f"{MS_GRAPH_BASE_URL}/me/drive/root/children"
    response = httpx.get(url, headers=headers)
    if response.status_code == 200:
        files = response.json().get("value", [])
        for file in files:
            print(f"Name: {file['name']}, ID: {file['id']}")
    else:
        print("Error fetching files:", response.text)

def list_folder_children(folder_id, headers):
    url = f"{MS_GRAPH_BASE_URL}/me/drive/items/{folder_id}/children"
    response = httpx.get(url, headers=headers)
    if response.status_code == 200:
        files = response.json().get("value", [])
        for file in files:
            print(f"Name: {file['name']}, ID: {file['id']}")
    else:
        print("Error fetching files:", response.text)

def main():
    load_dotenv()

    application_id = os.getenv("APPLICATION_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    scopes = ["Files.ReadWrite.All", "User.Read"]

    try:
        access_token = get_access_token(application_id, client_secret, scopes)
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        print("Files in Root Folder:")
        list_root_folder(headers)

        # Example: List children of a specific folder by ID
        folder_id = input("Enter folder ID to list its children (or press Enter to skip): ")
        if folder_id:
            print(f"Files in Folder ID {folder_id}:")
            list_folder_children(folder_id, headers)

    except Exception as e:
        print("Error:", e)
    
main()