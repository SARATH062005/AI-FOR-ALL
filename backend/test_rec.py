import requests
import json

# First login to get token
url_login = "http://localhost:8000/token"
login_data = {
    "username": "SA",
    "password": "testpassword", # I'll assume they used the same one OR I'll check it
    "email": ""
}

try:
    login_resp = requests.post(url_login, json=login_data)
    token = login_resp.json().get("access_token")
    print(f"Token: {token[:10]}...")

    # Now get recommendations
    url_rec = "http://localhost:8000/recommendations"
    headers = {"Authorization": f"Bearer {token}"}
    
    rec_resp = requests.get(url_rec, headers=headers)
    print(f"Status Code: {rec_resp.status_code}")
    print(f"Response: {json.dumps(rec_resp.json(), indent=2)[:500]}...")
except Exception as e:
    print(f"Error: {e}")
