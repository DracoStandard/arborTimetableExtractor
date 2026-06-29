import os
import json
import requests


def get_api_base_url() -> str:
    url = os.getenv("WFA_URL")
    if not url:
        raise ValueError("WFA_URL environment variable is missing.")
    return url.rstrip("/")


def get_headers(api_key: str = None) -> dict:
    headers = {"Content-Type": "application/json"}
    key = api_key or os.getenv("WFA_API_KEY")
    if key:
        headers["X-Api-Key"] = key
    return headers


def upload_json_file(data, api_key: str = None) -> bool:
    base_url = get_api_base_url()
    url = f"{base_url}/api/Timetable/import-raw"
    headers = get_headers(api_key)

    response = requests.post(url, data=json.dumps(data), headers=headers)

    if not response.ok:
        print(f"Upload failed - Status: {response.status_code}")
        print(f"Response: {response.text}")
        return False

    print("Upload successful")
    return True
