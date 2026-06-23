import requests
import re
import pandas as pd


import os
from dotenv import load_dotenv

def fetch_data(url: str, headers: dict) -> dict | list:
   #"""Fetch JSON data from API."""
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def extract_course_codes(data: dict | list) -> list[dict]:
    #"""Extract UPN and course codes from JSON data."""
    pattern = r"\b\d{2}[A-Za-z]/[A-Za-z]{2}\d\b|\b\d[A-Za-z]/[A-Za-z]{2}\d\b"
    rows = []

    if isinstance(data, list):
        for student in data:
            upn = student.get("UPN")
            courses = student.get("Courses/classes", "")
            codes = re.findall(pattern, courses)

            for code in codes:
                rows.append({"UPN": upn, "CourseCode": code})

    else:
        upn = data.get("UPN")
        courses = data.get("Courses/classes", "")
        codes = re.findall(pattern, courses)

        for code in codes:
            rows.append({"UPN": upn, "CourseCode": code})

    return rows


def create_dataframe(rows: list[dict]) -> pd.DataFrame:
    #"""Convert extracted rows into a DataFrame."""
    return pd.DataFrame(rows)


def save_to_csv(df: pd.DataFrame, filename: str) -> None:
    #"""Save DataFrame to CSV."""
    df.to_csv(filename, index=False)


def main():
    url = os.getenv("API_URL")
    auth = os.getenv("API_AUTH")

    headers = {
        "Authorization": auth
    }

    data = fetch_data(url, headers)
    rows = extract_course_codes(data)
    df_tt = create_dataframe(rows)

    print(df_tt)
    save_to_csv(df_tt, "upn_course_codes.csv")



if __name__ == "__main__":
    main()



