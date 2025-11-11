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
        root_folder = list_root_folder(headers)
        for folder in root_folder: 
            if 'folder' in folder:
                print(f'Folder id: {folder["id"]}')
                print(f'Folder name: {folder["name"]}')
                print (f'Folder web url: {folder["webUrl"]}')
                print(f'Folder size: {folder["size"]}')
                print(f'Folder created date: {folder["createdDateTime"]}')
                print (f'Created by: {folder["createdBy"]["user"]["displayName"]}) ')
                print(f'Folder modified date: {folder["lastModifiedDateTime"]}')
                print (f'Last modified by: {folder["lastModifiedBy"]["user"]["displayName"]}')
                print(f'Folder parent id: {folder["parentReference"]["id"]}')
                print (f'Item Count: {folder["folder"]["childCount"]}')
                print('-' * 50)
            elif 'file' in folder:
                print(f'File id: {folder["id"]}')
                print(f'File name: {folder["name"]}')
                print(f'File web url: {folder["webUrl"]}')
                print(f'File size (in KB): {folder["size"] / 1024:.2f}')
                print(f'File created date: {folder["createdDateTime"]}')
                print (f'Created by: {folder[" createdBy" ]["user"]["displayName"]}')
                print(f'File modified date: {folder["lastModifiedDateTime"]}')
                print (f'Last modified by: {folder["lastModifiedBy"]["user"]["displayName"]}')
                print(f'File parent id: {folder["parentReference"]["id"]}')
                print(f'File Mime type: {folder["file"]["mimeType"]}')
                print('-' * 50)
            print('-' * 50)
        folder_id = os.getenv("ROOT_FOLDER_ID")
        list_children = list_folder_children(headers, folder_id)
        for child in list_children: 
            if 'folder' in child:
                print(f'Folder id: {child["id"]}')
                print(f' Folder name: {child["name"]}')
                print(f' Folder web url: {child["webUrl"]}')
                print(f'Folder size: {child["size"]}')
                print (f'Folder created date: {child["createdDateTime"]}')
                print(f'Created by: {child["createdBy"]["user"][ "displayName"]}')
                print(f' Folder modified date: {child["lastModifiedDateTime"]}')
                print(f' Last modified by: {child["lastModifiedBy"]["user"]["displayName" ]} ')
                print (f'Folder parent id: {child["parentReference"]["id"]}')
                print(f'Item Count: {child["folder"]["childCount"]}')
            elif 'file' in child:
                print (f'File id: {child["id"]}')
                print(f'File name: {child["name"]}')
                print(f'File web url: {child["webUrl"]}')
                print(f'File size (in KB): {child["size"] / 1024:.2f}')
                print(f'File created date: {child["createdDateTime"]}')
                print(f'Created by: {child["createdBy"]["user"]["displayName"]}')
                print(f'File modified date: {child["lastModifiedDateTime"]}')
                print(f'Last modified by: {child["lastModifiedBy"]["user"]["displayName"]}')
                print(f'File parent id: {child["parentReference"]["id"]}')
                print(f'File Mime type: {child["file"]["mimeType"]}')
            print('-' * 50)
    except Exception as e:
        print("Error:", e)
    
main()