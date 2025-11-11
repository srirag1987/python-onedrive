import os
import webbrowser
import msal
from dotenv import load_dotenv

def get_access_token(application_id, client_secret, scopes):
    client = msal.ConfidentialClientApplication(
        client_id=application_id,
        client_credential=client_secret,
        authority="https://login.microsoftonline.com/consumers"
    )

    auth_request_url = client.get_authorization_request_url(scopes)
    webbrowser.open(auth_request_url)
    authorization_code = input("Enter authorization code: ")

    token_response = client.acquire_token_by_authorization_code(
        code=authorization_code,
        scopes=scopes
    )

    if "access_token" in token_response:
        return token_response["access_token"]
    else:
        raise Exception("Failed to acquire access token: " + str(token_response))
    

def main():
    load_dotenv()

    application_id = os.getenv("APPLICATION_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    scopes = ["Files.ReadWrite.All", "User.Read"]

    try:
        access_token = get_access_token(application_id, client_secret, scopes)
        print("Access Token:", access_token)
    except Exception as e:
        print("Error:", e)

main()