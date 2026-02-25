import sqlite3
import os

db_path = "sql_app.db"

if not os.path.exists(db_path):
    print(f"Database file {db_path} not found.")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("--- PROFILES TABLE CONTENT ---")
        cursor.execute("SELECT * FROM profiles")
        cols = [description[0] for description in cursor.description]
        print(f"Columns: {cols}")
        rows = cursor.fetchall()
        for row in rows:
            print(dict(zip(cols, row)))
                
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
