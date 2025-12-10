
import os
from dotenv import load_dotenv

load_dotenv()
val = os.getenv('DATABASE_URL')
# Print as repr to see hidden chars
print(f"RAW_VALUE_REPR={repr(val)}")
