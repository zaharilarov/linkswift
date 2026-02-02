""" *** INSTRUCTIONS (Type: Feature) *** Goal: Create the service layer to handle URL shortening logic. Scope: Implement string generation and a robust "shorten" function that handles database interactions and potential ID collisions.

*** SPECIFICATION *** Files:

service.py:

generate_random_code(length=6): Use string.ascii_letters and string.digits to return a random string.

shorten_url(original_url):

Input: A string (URL).

Action: Generate a code, try to INSERT it into links.

Collision Handling: Use a try/except sqlite3.IntegrityError block. If the code exists, retry generation (max 3 attempts).

Return: The resulting short_code.

test_service.py: A simple script to call shorten_url("https://google.com") and print the result.

*** CONTEXT REFERENCE *** Refer to context.md for table structure. Use get_db_connection from database.py.

*** IMPORTANT CONSTRAINTS ***

No ORM: Use raw cursor.execute("INSERT INTO ...").

Clean-up: Always close the database connection in a finally block.

Validation: Check if original_url is a non-empty string before proceeding. """