import sqlite3
import logging

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
