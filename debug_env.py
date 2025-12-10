
import os
from dotenv import load_dotenv

# Load .env manually to be sure
load_dotenv()

db_url = os.getenv('DATABASE_URL')
print(f"DEBUG: DATABASE_URL value: '{db_url}'")
if db_url:
    from sqlalchemy.engine.url import make_url
    try:
        u = make_url(db_url)
        print(f"Parsed URL: driver={u.drivername}, host={u.host}, port={u.port}, db={u.database}")
    except Exception as e:
        print(f"SQLAlchemy parse error: {e}")
else:
    print("DATABASE_URL is None")
