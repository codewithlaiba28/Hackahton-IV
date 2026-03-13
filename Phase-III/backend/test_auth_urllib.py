import urllib.request
import json
import socket

data = json.dumps({
    "email": "verify_fix@example.com",
    "password": "password",
    "name": "Verify Fix"
}).encode('utf-8')

req = urllib.request.Request(
    "http://localhost:8000/auth/register",
    data=data,
    headers={'Content-Type': 'application/json'}
)

try:
    with urllib.request.urlopen(req, timeout=10) as response:
        print("Status Code:", response.getcode())
        print("Response:", response.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print("HTTP Error:", e.code)
    print("Response Body:", e.read().decode('utf-8'))
except Exception as e:
    print("Error:", str(e))
