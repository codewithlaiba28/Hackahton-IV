
import sqlite3

def check_user():
    db_path = "backend/course_companion.db"
    email = "laibakhan@gmail.com"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT email, tier, api_key FROM users WHERE email=?", (email,))
        row = cursor.fetchone()
        
        if row:
            print(f"USER_FOUND: {row[0]}")
            print(f"TIER: {row[1]}")
            # print(f"API_KEY: {row[2]}")
        else:
            print(f"USER_NOT_FOUND: {email}")
            
        conn.close()
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    check_user()
