"""
Migration script to add multiple Telegram token support to bots table.
Run this with: python migrations/add_multiple_tokens.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db

def migrate():
    app = create_app()

    with app.app_context():
        print("Adding multiple Telegram token support to bots table...")

        try:
            # Check if columns already exist
            result = db.engine.execute("""
                SELECT column_name FROM information_schema.columns
                WHERE table_name = 'bots' AND column_name = 'telegram_token_1'
            """)

            if result.fetchone():
                print("✅ Columns already exist, skipping migration")
                return

            # Add new columns for multiple tokens
            db.engine.execute("""
                ALTER TABLE bots
                ADD COLUMN telegram_token_1 VARCHAR(100),
                ADD COLUMN telegram_token_2 VARCHAR(100),
                ADD COLUMN telegram_token_3 VARCHAR(100)
            """)

            print("✅ Multiple token columns added successfully!")

            # If there's existing telegram_token data, move it to telegram_token_1
            result = db.engine.execute("SELECT id, telegram_token FROM bots WHERE telegram_token IS NOT NULL")
            migrated_count = 0
            for row in result:
                db.engine.execute(
                    "UPDATE bots SET telegram_token_1 = %s WHERE id = %s",
                    (row[1], row[0])
                )
                migrated_count += 1

            if migrated_count > 0:
                print(f"✅ Migrated existing tokens for {migrated_count} bots")

        except Exception as e:
            print(f"⚠️ Migration may have failed or columns already exist: {e}")

        print("✅ Migration completed!")

if __name__ == '__main__':
    migrate()
