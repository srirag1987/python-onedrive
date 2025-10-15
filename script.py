import asyncio
import requests
import json
from azure.identity import InteractiveBrowserCredential
from typing import List, Dict

# --- CONFIGURATION ---
CLIENT_ID = "6cabd44e-7262-4115-971b-22360a7ea5b6"
TENANT_ID = "76644521-0283-488a-b85d-cb97e852bcf9"
SCOPES = ['Files.Read.All']
# TARGET_FOLDER_PATH is now only used for the first step (ID resolution)
TARGET_FOLDER_PATH = "Documents/Germany" 
GRAPH_API_BASE_URL = "https://graph.microsoft.com/v1.0/"

# --- HELPER FUNCTIONS ---

async def authenticate_client(client_id: str, scopes: List[str]) -> str:
    """Authenticates and returns the access token."""
    print("Authenticating... A browser window will open for sign-in.")
    
    credential = InteractiveBrowserCredential(

        client_id=client_id,
        tenant_id=TENANT_ID
    )
    
    token_response = credential.get_token(*scopes)
    
    if token_response.token:
        print("Authentication successful.")
        return token_response.token
    else:
        raise Exception("Failed to retrieve access token.")

def get_item_id_by_path(access_token: str, folder_path: str) -> str | None:
    """
    Step 1: Get the unique DriveItem ID for a given path.
    API: /me/drive/root:/Documents/Germany
    """
    print(f"\n--- 1. Resolving ID for path: /{folder_path} ---")
    
    # Endpoint to resolve the item by path (without the /children suffix)
    endpoint = f"{GRAPH_API_BASE_URL}me/drive/root:/{folder_path}"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    try:
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status() 
        data = response.json()
        
        # Check if the item is actually a folder
        if 'folder' not in data:
            print(f"Error: Item at /{folder_path} is not a folder.")
            return None
        
        print(f"Successfully resolved ID: {data.get('id')}")
        return data.get('id')

    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error occurred during ID resolution: {err}")
        try:
            error_data = err.response.json()
            error_message = error_data.get('error', {}).get('message', 'Unknown error.')
            print(f"API Error Message: {error_message}")
        except json.JSONDecodeError:
            pass
        return None
    
def list_folders_by_id(access_token: str, item_id: str) -> List[Dict] | None:
    """
    Step 2: Lists all folders inside a specific DriveItem ID.
    API: /me/drive/items/{item-id}/children
    """
    print(f"\n--- 2. Listing children by ID: {item_id} ---")
    
    # Endpoint using the unique item ID
    endpoint = f"{GRAPH_API_BASE_URL}me/drive/items/{item_id}/children"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    params = {
        "$filter": "folder ne null"  # Filter to include only folders
    }

    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status() 

        data = response.json()
        
        folders = []
        for item in data.get('value', []):
            if 'folder' in item:
                folders.append({
                    "name": item.get('name'),
                    "id": item.get('id'),
                    "child_count": item.get('folder', {}).get('childCount')
                })
        
        return folders

    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error occurred during children listing: {err}")
        try:
            error_data = err.response.json()
            error_message = error_data.get('error', {}).get('message', 'Unknown error.')
            print(f"API Error Message: {error_message}")
        except json.JSONDecodeError:
            pass
        return None

# --- MAIN EXECUTION ---

async def main():
    if CLIENT_ID == "YOUR_CLIENT_ID":
        print("ERROR: Please update the CLIENT_ID variable with your application's Client ID.")
        return

    try:
        # 1. Authenticate and get the token
        access_token = await authenticate_client(CLIENT_ID, SCOPES)
        
        # 2. Get the unique ID for the target path
        target_id = get_item_id_by_path(access_token, TARGET_FOLDER_PATH)
        
        if not target_id:
            print(f"\nCould not resolve the path '{TARGET_FOLDER_PATH}'. Aborting.")
            return

        # 3. List Folders using the Item ID
        folders = list_folders_by_id(access_token, target_id)
        
        if folders is not None:
            if folders:
                print(f"\nFound {len(folders)} folders in '/{TARGET_FOLDER_PATH}':")
                for folder in folders:
                    print(f"  Folder Name: {folder['name']}, Children Count: {folder['child_count']}")
            else:
                print(f"No folders found in path '{TARGET_FOLDER_PATH}'.")
        else:
            print(f"Failed to retrieve folder list for '{TARGET_FOLDER_PATH}'.")

    except Exception as e:
        print(f"\nAn unexpected error occurred during the main process: {e}")
        
if __name__ == "__main__":
    asyncio.run(main())