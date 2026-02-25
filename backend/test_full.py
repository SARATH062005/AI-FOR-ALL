import requests
import json

BASE_URL = "http://localhost:8000"

def test_full_flow():
    # 1. Register
    reg_data = {
        "username": "debuguser",
        "password": "debugpassword",
        "email": "debug@example.com"
    }
    requests.post(f"{BASE_URL}/register", json=reg_data)
    
    # 2. Login
    login_resp = requests.post(f"{BASE_URL}/token", json=reg_data)
    token = login_resp.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Create Profile
    profile_data = {
        "full_name": "Debug User",
        "skills": "Python, FastAPI, AI",
        "experience": "Built a portal and tested it manually.",
        "education": "BS Computer Science",
        "summary": "Looking for AI engineering roles."
    }
    requests.post(f"{BASE_URL}/profile", json=profile_data, headers=headers)
    
    # 4. Get Recommendations
    rec_resp = requests.get(f"{BASE_URL}/recommendations", headers=headers)
    print(f"Status: {rec_resp.status_code}")
    print(f"Outcome: {json.dumps(rec_resp.json(), indent=2)}")

if __name__ == "__main__":
    test_full_flow()
