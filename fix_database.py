"""
Database fix script - add multiple token columns
"""
import sqlite3
import os

def fix_database():
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'botfactory.db')
    
    if not os.path.exists(db_path):
        print("❌ Database file not found!")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if columns exist
        cursor.execute("PRAGMA table_info(bots)")
        columns = [column[1] for column in cursor.fetchall()]
        
        print(f"📋 Current columns: {columns}")
        
        # Add new columns if they don't exist
        if 'telegram_token_1' not in columns:
            cursor.execute("ALTER TABLE bots ADD COLUMN telegram_token_1 VARCHAR(100)")
            print("✅ Added telegram_token_1 column")
        
        if 'telegram_token_2' not in columns:
            cursor.execute("ALTER TABLE bots ADD COLUMN telegram_token_2 VARCHAR(100)")
            print("✅ Added telegram_token_2 column")
            
        if 'telegram_token_3' not in columns:
            cursor.execute("ALTER TABLE bots ADD COLUMN telegram_token_3 VARCHAR(100)")
            print("✅ Added telegram_token_3 column")
        
        # Migrate existing telegram_token data to telegram_token_1
        if 'telegram_token' in columns:
            cursor.execute("""
                UPDATE bots 
                SET telegram_token_1 = telegram_token 
                WHERE telegram_token IS NOT NULL AND telegram_token_1 IS NULL
            """)
            migrated = cursor.rowcount
            if migrated > 0:
                print(f"✅ Migrated {migrated} existing tokens to telegram_token_1")
        
        conn.commit()
        print("✅ Database updated successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    fix_database()
