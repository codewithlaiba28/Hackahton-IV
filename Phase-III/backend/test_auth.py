import requests

try:
    res = requests.post(
        "http://localhost:8000/auth/register",
        json={"email": "test@test.com", "password": "password", "name": "Test"}
    )
    print("Status:", res.status_code)
    print("Response:", res.text)
except Exception as e:
    print("Error:", str(e))
