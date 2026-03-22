from config import *
from ms_graph import get_access_token
from graph_service import get_site_id, get_cad_drive_id, list_files

from db import engine, get_db
from models import Base, FileRecord


def main():

    # Create table if not exists
    Base.metadata.create_all(bind=engine)

    print("🔐 Getting access token...")
    token = get_access_token(APPLICATION_ID, CLIENT_SECRET, TENANT_ID)

    headers = {
        "Authorization": f"Bearer {token}"
    }

    print("🌐 Fetching SharePoint data...")
    site_id = get_site_id(headers, SITE_HOSTNAME, SITE_PATH)
    drive_id = get_cad_drive_id(headers, site_id)
    items = list_files(headers, site_id, drive_id)

    print("💾 Saving to SQL Server...")
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
    db.close()

    print("✅ Data saved successfully!")


if __name__ == "__main__":
    main()