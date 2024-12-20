from datetime import datetime, timezone
import json
from pathlib import Path
import sys

import requests


def get_agency_url(agency: str):
    path = Path("./metadata.json")
    if not path.exists():
        raise RuntimeError("Metadata file not found")

    config = json.loads(path.read_text())
    return config[agency]


def check_metadata_timestamp(url):
    now = datetime.now(tz=timezone.utc)
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    data = response.json()
    ts = data["db"]["timestamp"]
    timestamp = datetime.fromisoformat(ts)

    if not all((timestamp.year == now.year, timestamp.month == now.month, timestamp.day == now.day)):
        raise RuntimeError(f"Database timestamp mismatch: {ts}")


if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        raise RuntimeError("Usage: check-metadata AGENCY")

    agency = args[1]
    url = get_agency_url(agency)
    check_metadata_timestamp(url)
