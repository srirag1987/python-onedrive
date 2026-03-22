import json
from datetime import datetime

from config import *
from ms_graph import get_access_token
from graph_service import get_site_id, get_cad_drive_id, list_files

from db import engine, get_db
from models import Base, Project, Country


def parse_datetime(dt_str):
    if not dt_str:
        return None
    return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))


def main():

    Base.metadata.create_all(bind=engine)

    print("🔐 Getting token...")
    token = get_access_token(APPLICATION_ID, CLIENT_SECRET, TENANT_ID)

    headers = {
        "Authorization": f"Bearer {token}"
    }

    print("📡 Fetching data...")
    site_id = get_site_id(headers, SITE_HOSTNAME, SITE_PATH)
    drive_id = get_cad_drive_id(headers, site_id)
    items = list_files(headers, site_id, drive_id)

    db = get_db()

    print("💾 Saving folders to projects table...\n")

    for item in items:

        # ✅ Only folders (parent level)
        if "folder" not in item:
            continue

        folder_name = item.get("name")
        web_url = item.get("webUrl")

        created = parse_datetime(item.get("createdDateTime"))
        modified = parse_datetime(item.get("lastModifiedDateTime"))

        # ✅ Avoid duplicates
        existing = db.query(Project).filter_by(name=folder_name).first()
        if existing:
            print(f"Skipping existing: {folder_name}")
            continue

        project = Project(
            name=folder_name,
            web_url=web_url,
            created_at_graph=created,
            last_modified=modified,
            raw_json=json.dumps(item)  # store full response
        )

        db.add(project)

        # 🌍 OPTIONAL: extract country from name (example logic)
        # e.g. "Germany_Project1"
        if "_" in folder_name:
            country_name = folder_name.split("_")[0]

            country = db.query(Country).filter_by(name=country_name).first()

            if not country:
                country = Country(name=country_name)
                db.add(country)

            project.countries.append(country)

    db.commit()
    db.close()

    print("\n✅ Projects saved successfully!")


if __name__ == "__main__":
    main()