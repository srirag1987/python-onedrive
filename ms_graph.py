import os
import webbrowser
import msal
from dotenv import load_dotenv

MS_GRAPH_BASE_URL = "https://graph.microsoft.com/v1.0"

def get_access_token(application_id, client_secret, scopes):
    client = msal.ConfidentialClientApplication(
        client_id=application_id,
        client_credential=client_secret,
        authority="https://login.microsoftonline.com/2019dd21-44d9-4bf8-8b6e-aeeba882c8b9"
    )

    token_result = client.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])

    if "access_token" in token_result:
        return token_result["access_token"]
    else:
        raise Exception("Failed to acquire access token: " + str(token_result))
 

def main():
    load_dotenv()

    application_id = os.getenv("APPLICATION_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    scopes=["https://graph.microsoft.com/.default"]

    try:
        access_token = get_access_token(application_id, client_secret, scopes)
        print("Access Token:", access_token)
    except Exception as e:
        print("Error:", e)

main()