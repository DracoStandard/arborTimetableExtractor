import requests
import re

# URL and Authorization header
url = "https://weston-favell-academy.uk.arbor.sc/data-export/export/id/49/h/aaa41859072aa2f1/format/json/v/2/"
headers = {
    "Authorization": "Basic cGN1bW1pbnM6ZTJiN2Q5ODdiYWM4ZWUzYzg1MTVjZTk1NjNkODI1MGMzNTk5Y2IwOA=="
}

# Fetch JSON data
response = requests.get(url, headers=headers)
response.raise_for_status()  # Ensure request was successful
data = response.json()
# Regex pattern for course codes (handles KS3 and GCSE formats)
pattern = r"\b\d{2}[A-Za-z]/[A-Za-z]{2}\d\b|\b\d[A-Za-z]/[A-Za-z]{2}\d\b"

rows = []

# If data is a list of students
if isinstance(data, list):
    for student in data:
        upn = student.get("UPN")
        courses = student.get("Courses/classes", "")
        codes = re.findall(pattern, courses)
        for code in codes:
            rows.append({"upn": upn, "lesson": code})
else:
    # Single student record
    upn = data.get("upn")
    courses = data.get("lesson", "")
    codes = re.findall(pattern, courses)
    for code in codes:
        rows.append({"UPN": upn, "CourseCode": code})

# Create DataFrame
df_tt = pd.DataFrame(rows)

# Output
print(df_tt)

# Optional: Save to CSV
df_tt.to_csv("upn_course_codes.csv", index=False)
#print("Saved to upn_course_codes.csv")