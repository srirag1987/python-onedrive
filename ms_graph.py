import msal

MS_GRAPH_BASE_URL = "https://graph.microsoft.com/v1.0"


def get_access_token(application_id, client_secret, tenant_id):

    client = msal.ConfidentialClientApplication(
        client_id=application_id,
        client_credential=client_secret,
        authority=f"https://login.microsoftonline.com/{tenant_id}"
    )

    token = client.acquire_token_for_client(
        scopes=["https://graph.microsoft.com/.default"]
    )

    if "access_token" in token:
        return token["access_token"]

    raise Exception(str(token))