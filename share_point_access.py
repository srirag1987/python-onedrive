import requests, os

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Accept": "application/json"
}

# Example: Get SharePoint Site info
hostname = "yourtenant.sharepoint.com"
site_path = "/sites/CAD"

url = f"https://graph.microsoft.com/v1.0/sites/{hostname}:{site_path}"
response = requests.get(url, headers=headers)

print(response.status_code)
print(response.json())
