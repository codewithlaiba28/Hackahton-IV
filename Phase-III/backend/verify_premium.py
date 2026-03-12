import urllib.request
import json

BASE_URL = "http://127.0.0.1:8000"
API_KEY = "test_api_key_12345"

def make_request(url, api_key=None):
    headers = {}
    if api_key:
        headers["X-API-Key"] = api_key
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            return response.getcode(), json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:
        return 500, str(e)

def test_premium_access():
    print("--- Phase 1: Premium Access Test ---")
    
    # 1. Test a Free Chapter (Should work)
    print("\n[1] Testing Free Chapter (ch-001)...")
    code1, data1 = make_request(f"{BASE_URL}/chapters/ch-001", API_KEY)
    print(f"Status: {code1}")
    if code1 == 200:
        print(f"Result: SUCCESS (Accessible)")
    
    # 2. Test a Premium Chapter (Should work because user is premium)
    print("\n[2] Testing Premium Chapter (ch-004)...")
    code2, data2 = make_request(f"{BASE_URL}/chapters/ch-004", API_KEY)
    print(f"Status: {code2}")
    if code2 == 200:
        print(f"Result: SUCCESS (Premium Unlock Verified)")
        print(f"Chapter: {data2['data']['title']}")
    
    # 3. Test Unauthorized Access (Should fail)
    print("\n[3] Testing Unauthorized Request (No API Key)...")
    code3, data3 = make_request(f"{BASE_URL}/chapters/ch-004") 
    print(f"Status: {code3}")
    if code3 == 401:
        print("Result: SUCCESS (Blocked as expected)")

if __name__ == "__main__":
    test_premium_access()
