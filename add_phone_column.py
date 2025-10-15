"""
User jadvaliga telefon raqam ustuni qo'shish
"""
import sqlite3
import os

def add_phone_column():
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'botfactory.db')
    
    if not os.path.exists(db_path):
        print("❌ Database file not found!")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if phone column already exists
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'phone' in columns:
            print("✅ Phone column already exists!")
            return
        
        # Add phone column
        cursor.execute("ALTER TABLE users ADD COLUMN phone VARCHAR(20)")
        conn.commit()
        
        print("✅ Phone column added successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    add_phone_column()
