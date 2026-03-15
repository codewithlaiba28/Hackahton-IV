import urllib.request
import json

# Using the email from the previous successful registration test would be better, 
# but I'll use the one I just registered to be sure.
# Wait, let's just use the one from test_auth_fresh.py if it was printed.
# Or just register a new one and then login.

import uuid
email = f"login_test_{uuid.uuid4().hex[:8]}@example.com"
password = "testpassword123"

# 1. Register
reg_data = json.dumps({
    "email": email,
    "password": password,
    "name": "Login Tester"
}).encode('utf-8')

reg_req = urllib.request.Request(
    "http://localhost:8000/auth/register",
    data=reg_data,
    headers={'Content-Type': 'application/json'}
)

try:
    with urllib.request.urlopen(reg_req, timeout=10) as response:
        print("Registration Status:", response.getcode())
        
    # 2. Login
    login_data = json.dumps({
        "email": email,
        "password": password
    }).encode('utf-8')

    login_req = urllib.request.Request(
        "http://localhost:8000/auth/login",
        data=login_data,
        headers={'Content-Type': 'application/json'}
    )

    with urllib.request.urlopen(login_req, timeout=10) as response:
        print("Login Status:", response.getcode())
        print("Login Response:", response.read().decode('utf-8'))

except urllib.error.HTTPError as e:
    print("HTTP Error:", e.code)
    print("Response Body:", e.read().decode('utf-8'))
except Exception as e:
    print("Error:", str(e))
