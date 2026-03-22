import httpx
from shared.ms_graph import MS_GRAPH_BASE_URL


def get_site_id(headers, hostname, path):
    url = f"{MS_GRAPH_BASE_URL}/sites/{hostname}:{path}"
    return httpx.get(url, headers=headers).json()["id"]


def get_cad_drive_id(headers, site_id):
    url = f"{MS_GRAPH_BASE_URL}/sites/{site_id}/drives"
    drives = httpx.get(url, headers=headers).json()["value"]

    for d in drives:
        if d["name"] == "CAD":
            return d["id"]

    raise Exception("CAD drive not found")


def list_files(headers, site_id, drive_id):
    url = f"{MS_GRAPH_BASE_URL}/sites/{site_id}/drives/{drive_id}/root/children"
    return httpx.get(url, headers=headers).json()["value"]