import requests
import json
import os

BASE_URL = "http://localhost:8000"

# Register/Login
reg_data = {"username": "typecheck", "password": "password", "email": "type@check.com"}
requests.post(f"{BASE_URL}/register", json=reg_data)
token = requests.post(f"{BASE_URL}/token", json=reg_data).json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Create Profile
profile_data = {"full_name": "Type Checker", "skills": "Python", "experience": "N/A", "education": "N/A", "summary": "N/A"}
requests.post(f"{BASE_URL}/profile", json=profile_data, headers=headers)

# Get Recommendations
rec = requests.get(f"{BASE_URL}/recommendations", headers=headers).json()

print("COURSE TYPE CHECK:")
if rec.get("courses"):
    tags = rec["courses"][0].get("tags")
    print(f"Tags type: {type(tags)} | Value: {tags}")

print("\nJOB TYPE CHECK:")
if rec.get("jobs"):
    skills = rec["jobs"][0].get("required_skills")
    print(f"Skills type: {type(skills)} | Value: {skills}")
