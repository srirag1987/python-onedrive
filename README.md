Here is a complete `README.md` file for your Python script, which connects to OneDrive using the Microsoft Graph API. It includes setup instructions, configuration details, and execution steps.

# 📂 OneDrive Graph API Python Connector

This project provides a Python script to authenticate with Microsoft Graph and list the folders within a specific path in a user's OneDrive, using the most resilient method to bypass potential SharePoint Online (SPO) licensing checks.

-----

## 🚀 Getting Started

### Prerequisites

1.  **Python 3.8+**
2.  **Azure App Registration:** You must register an application in the Azure Portal to get a **Client ID** and configure permissions.

### 1\. Azure Portal Setup

1.  Go to the [Azure Portal App Registrations](https://www.google.com/search?q=https://portal.azure.com/%23view/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/~/RegisteredApps).
2.  Create a **New Registration**.
3.  Set **Supported account types** to: **Accounts in any organizational directory (Any Microsoft Entra ID tenant - Multitenant) and personal Microsoft accounts (e.g., Skype, Xbox)**.
4.  Navigate to **API permissions**:
      * Add a permission: **Microsoft Graph** $\rightarrow$ **Delegated permissions**.
      * Select **`Files.Read.All`**.
      * Click **Grant admin consent** (if available and needed for your account type).
5.  Navigate to **Authentication**:
      * Click **+ Add a platform** $\rightarrow$ **Mobile and desktop applications**.
      * Add a **Redirect URI**: `http://localhost`
      * Under **Default client type**, ensure **Treat application as a public client** is set to **Yes**.

### 2\. Installation

Install the required Python libraries:

```bash
pip install msgraph-sdk azure-identity requests
```

-----

## ⚙️ Configuration

Open the `script.py` file and update the following variables with your specific values:

| Variable | Description | Your Value |
| :--- | :--- | :--- |
| `CLIENT_ID` | Your Application (Client) ID from the Azure Portal. | `"6cabd44e-7262-4115-971b-22360a7ea5b6"` |
| `TARGET_FOLDER_PATH` | The path to the folder you want to inspect, relative to your OneDrive root. | `"Documents/Germany"` |

**Example Configuration in `script.py`:**

```python
# --- CONFIGURATION ---
CLIENT_ID = "YOUR_CLIENT_ID" # e.g., "6cabd44e-7262-4115-971b-22360a7ea5b6"
SCOPES = ['Files.Read.All']
TARGET_FOLDER_PATH = "Documents/Germany" 
```

-----

## 💻 How to Run

Execute the script from your terminal:

```bash
python3 script.py
```

### Execution Flow:

1.  **Authentication:** A browser window will automatically open, prompting you to sign in to your Microsoft account and grant the application permissions.
2.  **Token Exchange:** After successful sign-in, the script will receive an access token.
3.  **API Call:** The script uses the explicit `/me/drives/ID/root:/...` endpoint to list the contents of your specified folder, reliably accessing your personal OneDrive storage.
4.  **Output:** The names and child counts of all subfolders within the target path will be printed to the console.

### Example Output

```
Authenticating... A browser window will open for sign-in.
Authentication successful.

--- Listing Folders in Path: /me/drives/ID/root:/Documents/Germany ---

Found 3 folders in '/Documents/Germany':
  Folder Name: Berlin Trip, Children Count: 5
  Folder Name: Tax Documents 2024, Children Count: 12
  Folder Name: Recipes, Children Count: 8
```

-----

## 🛠️ Technical Details

This script implements a resilient two-part authentication and API calling method:

1.  **Asynchronous Authentication:** Uses `azure-identity`'s `InteractiveBrowserCredential` with `tenant_id="common"` to support both personal and work/school accounts.
2.  **Direct `requests` Call:** Bypasses the complex `msgraph-sdk` internal methods and uses the simple `requests` library to make the direct API call.
3.  **Explicit Drive ID:** The endpoint `me/drives/ID/root:/...` is used to explicitly target the user's default OneDrive drive (using the `ID` alias), which is essential to avoid the "**Tenant does not have a SPO license**" error when dealing with certain account configurations.
