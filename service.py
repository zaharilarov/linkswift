import string
import random
import sqlite3
import logging
from database import get_db_connection

def generate_random_code(length: int = 6) -> str:
    """Generates a random alphanumeric string of a given length."""
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))

def shorten_url(original_url: str) -> str | None:
    """
    Validates the URL, generates a short code, and persists it in the database.
    Handles collisions by retrying generation up to 3 times.
    """
    if not isinstance(original_url, str) or not original_url.strip():
        logging.error("Invalid URL: Must be a non-empty string.")
        return None

    # Normalize URL: strip whitespace and ensure protocol
    original_url = original_url.strip()
    if not (original_url.startswith("http://") or original_url.startswith("https://")):
        original_url = f"https://{original_url}"

    conn = get_db_connection()
    if conn is None:
        return None

    max_retries = 3
    attempts = 0

    try:
        while attempts < max_retries:
            short_code = generate_random_code(6)
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO links (original_url, short_code) VALUES (?, ?)",
                    (original_url, short_code)
                )
                conn.commit()
                return short_code
            except sqlite3.IntegrityError:
                attempts += 1
                logging.warning(f"Collision detected for code {short_code}. Retry {attempts}/{max_retries}")
        
        logging.error("Failed to generate a unique short code after 3 attempts.")
        return None
    except sqlite3.Error as e:
        logging.error(f"Database error during URL shortening: {e}")
        return None
    finally:
        conn.close()
