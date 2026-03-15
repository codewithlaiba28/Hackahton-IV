
import sqlite3

def list_users():
    db_path = "backend/course_companion.db"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT email, tier, name FROM users")
        rows = cursor.fetchall()
        
        print(f"FOUND {len(rows)} USERS:")
        for row in rows:
            print(f"EMAIL: {row[0]} | TIER: {row[1]} | NAME: {row[2]}")
            
        conn.close()
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    list_users()
