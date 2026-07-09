import os
import pyodbc
from dotenv import load_dotenv
from pathlib import Path


dotenv_path = Path(".env").resolve()
print("Loading:", dotenv_path)

load_dotenv(dotenv_path=dotenv_path, override=True)

print("USERNAME =", os.getenv("DB_USERNAME"))

conn = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER=tcp:{os.getenv('SERVER')},1433;"
    f"DATABASE={os.getenv('DATABASE')};"
    f"UID={os.getenv('DB_USERNAME')};"
    f"PWD={os.getenv('DB_PASSWORD')};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

def get_connection():
    return pyodbc.connect(conn)