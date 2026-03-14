
import sqlite3

def check_schema():
    db_path = "backend/course_companion.db"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        
        print("COLUMNS IN 'users' TABLE:")
        for col in columns:
            print(f"ID: {col[0]} | NAME: {col[1]} | TYPE: {col[2]}")
            
        cursor.execute("SELECT * FROM users LIMIT 1")
        row = cursor.fetchone()
        if row:
            print("\nSAMPLE ROW:")
            print(row)
            
        conn.close()
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    check_schema()
