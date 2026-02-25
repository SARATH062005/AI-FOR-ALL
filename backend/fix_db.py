import sqlite3

db_path = "sql_app.db"

def fix_db():
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if profiles table has summary column
        cursor.execute("PRAGMA table_info(profiles)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'summary' not in columns:
            print("Adding 'summary' column to 'profiles' table...")
            cursor.execute("ALTER TABLE profiles ADD COLUMN summary TEXT")
            conn.commit()
            print("Successfully added 'summary' column.")
        else:
            print("'summary' column already exists.")
            
        conn.close()
    except Exception as e:
        print(f"Error fixing database: {e}")

if __name__ == "__main__":
    fix_db()
