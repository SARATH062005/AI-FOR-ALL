import sqlite3
import os

db_path = "sql_app.db"

if not os.path.exists(db_path):
    print(f"Database file {db_path} not found.")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("--- USERS ---")
        cursor.execute("SELECT id, username, email FROM users")
        users = cursor.fetchall()
        for user in users:
            print(f"ID: {user[0]} | User: {user[1]} | Email: {user[2]}")
            
        print("\n--- PROFILES ---")
        cursor.execute("SELECT user_id, full_name, skills FROM profiles")
        profiles = cursor.fetchall()
        if not profiles:
            print("No profiles found.")
        for p in profiles:
            print(f"UserID: {p[0]} | Name: {p[1]} | Skills: {p[2][:30]}...")
                
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
