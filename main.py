import requests
import re
import pandas as pd
from uploadDb import upload_json_file




import os
from dotenv import load_dotenv

def fetch_data(url: str, headers: dict) -> dict | list:
   #"""Fetch JSON data from API."""
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    
 # Save raw response
    with open("data.json", "w", encoding="utf-8") as f:
        f.write(response.text)


    return response.json()





def main():
    url = os.getenv("API_URL")
    auth = os.getenv("API_AUTH")

    headers = {
        "Authorization": auth
    }

    data = fetch_data(url, headers)

    upload_json_file(data)

if __name__ == "__main__":
    main()



