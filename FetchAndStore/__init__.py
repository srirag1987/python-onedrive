import json
import azure.functions as func

from shared.config import *
from shared.ms_graph import get_access_token
from shared.graph_service import get_site_id, get_cad_drive_id, list_files
from shared.db import get_db
from shared.models import FileRecord


def main(req: func.HttpRequest) -> func.HttpResponse:

    try:
        # 1️⃣ Get Token
        token = get_access_token(APPLICATION_ID, CLIENT_SECRET, TENANT_ID)

        headers = {
            "Authorization": f"Bearer {token}"
        }

        # 2️⃣ Fetch Data
        site_id = get_site_id(headers, SITE_HOSTNAME, SITE_PATH)
        drive_id = get_cad_drive_id(headers, site_id)
        items = list_files(headers, site_id, drive_id)

        # 3️⃣ Save to DB
        db = get_db()

        for item in items:
            if "folder" in item:
                record = FileRecord(
                    name=item["name"],
                    size_kb=0,
                    item_type="FOLDER"
                )
            else:
                record = FileRecord(
                    name=item["name"],
                    size_kb=int(item["size"] / 1024),
                    item_type="FILE"
                )

            db.add(record)

        db.commit()

        return func.HttpResponse(
            json.dumps({"message": "Data saved successfully"}),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)