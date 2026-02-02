import os
import sqlite3
import logging

# Render persistence: use /data/shortener.db if /data exists, otherwise local
if os.path.exists("/data"):
    DB_NAME = "/data/shortener.db"
else:
    DB_NAME = "shortener.db"

def get_db_connection() -> sqlite3.Connection | None:
    """
    Establishes a connection to the SQLite database.
    Configures the connection to use sqlite3.Row for dictionary-like access
    and enables foreign key support.
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn
    except sqlite3.Error as e:
        logging.error(f"Error connecting to database: {e}")
        return None
