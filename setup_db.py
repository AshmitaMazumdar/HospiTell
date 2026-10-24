"""
Hospitell Database Setup Script
--------------------------------
Creates the database (MySQL default, or SQLite fallback) and generates all ORM tables.

Usage:
  python setup_db.py              # Uses MySQL (default, reads from .env / config.json)
  python setup_db.py --sqlite     # Forces SQLite (creates local instance/fit_o_sphere.db)
"""

import os
import sys
import json
from dotenv import load_dotenv

load_dotenv()

# Check for CLI flag
if "--sqlite" in sys.argv:
    os.environ["USE_SQLITE"] = "true"

use_sqlite = os.getenv("USE_SQLITE", "false").lower() == "true"

if not use_sqlite:
    # Try MySQL first
    print("[*] Setting up MySQL database...")
    try:
        import pymysql
    except ImportError:
        print("[!] pymysql is not installed. Please run: pip install pymysql")
        sys.exit(1)

    # Load MySQL credentials from config.json or environment
    mysql_host = os.getenv("MYSQL_HOST", "localhost")
    mysql_user = os.getenv("MYSQL_USER", "root")
    mysql_password = os.getenv("MYSQL_PASSWORD", "")
    mysql_db = os.getenv("MYSQL_DB", "fit-o-sphere")

    try:
        with open("config.json", "r") as f:
            cfg = json.load(f).get("params", {})
            mysql_host = os.getenv("MYSQL_HOST") or cfg.get("mysql_host", "localhost")
            mysql_user = os.getenv("MYSQL_USER") or cfg.get("mysql_user", "root")
            mysql_password = os.getenv("MYSQL_PASSWORD") or cfg.get("mysql_password", "")
            mysql_db = os.getenv("MYSQL_DB") or cfg.get("mysql_db", "fit-o-sphere")
    except Exception:
        pass

    try:
        print(f"[*] Connecting to MySQL server at {mysql_host} as user '{mysql_user}'...")
        conn = pymysql.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            charset="utf8mb4"
        )
        with conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{mysql_db}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        conn.commit()
        conn.close()
        print(f"[+] Successfully ensured database `{mysql_db}` exists on MySQL!")
    except Exception as e:
        print(f"[!] Warning: Could not connect to MySQL server: {e}")
        print("[!] If MySQL is not installed or running, you can use SQLite instead by:")
        print("    1. Setting USE_SQLITE=true in your .env file, OR")
        print("    2. Running: python setup_db.py --sqlite")
        sys.exit(1)

# Now run db.create_all() inside Flask app context
print("[*] Initializing tables with SQLAlchemy db.create_all()...")
from app import app, db

with app.app_context():
    db.create_all()

print("[+] All tables created successfully!")
if use_sqlite:
    print("[+] Using SQLite database (stored in instance/fit_o_sphere.db)")
else:
    print(f"[+] Using MySQL database `{mysql_db}`")
