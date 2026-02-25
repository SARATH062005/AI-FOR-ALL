import sqlite3
import os

db_path = "sql_app.db"

def update_schema():
    if not os.path.exists(db_path):
        print(f"Database {db_path} not found.")
        return
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    new_columns = [
        ("phone", "TEXT"),
        ("location", "TEXT"),
        ("github_url", "TEXT"),
        ("linkedin_url", "TEXT"),
        ("portfolio_url", "TEXT"),
        ("languages", "TEXT")
    ]
    
    cursor.execute("PRAGMA table_info(profiles)")
    existing_columns = [col[1] for col in cursor.fetchall()]
    
    for col_name, col_type in new_columns:
        if col_name not in existing_columns:
            print(f"Adding column {col_name}...")
            cursor.execute(f"ALTER TABLE profiles ADD COLUMN {col_name} {col_type}")
        else:
            print(f"Column {col_name} already exists.")
            
    conn.commit()
    conn.close()
    print("Schema update complete.")

if __name__ == "__main__":
    update_schema()
