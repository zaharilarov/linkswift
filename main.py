from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import sqlite3
import logging
from init_db import init_db
from database import get_db_connection
from service import shorten_url

app = FastAPI(title="URL Shortener")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def startup_event():
    """
    Ensures the database is initialized on server start.
    Crucial for ephemeral environments like Render Free Tier.
    """
    init_db()

class URLRequest(BaseModel):
    url: str

@app.get("/")
async def read_root(request: Request):
    """
    Serves the main frontend page.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/recent")
async def get_recent_links():
    """
    Returns the last 5 created links with their click counts.
    """
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection error.")
    
    try:
        cursor = conn.cursor()
        # Join links and clicks to get the counts for the last 5 links
        cursor.execute("""
            SELECT l.short_code, l.original_url, COUNT(c.id) as click_count
            FROM links l
            LEFT JOIN clicks c ON l.id = c.link_id
            GROUP BY l.id
            ORDER BY l.created_at DESC
            LIMIT 5
        """)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        logging.error(f"Database error fetching recent links: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")
    finally:
        conn.close()

@app.post("/shorten", status_code=201)
async def create_short_url(request: URLRequest):
    """
    Creates a short code for the given original URL.
    """
    code = shorten_url(request.url)
    if not code:
        raise HTTPException(status_code=400, detail="Failed to shorten URL. Please check the URL format.")
    
    return {"short_url": f"http://localhost:8000/{code}"}

@app.get("/{short_code}")
async def redirect_to_original(short_code: str, request: Request):
    """
    Redirects to the original URL associated with the short code
    and logs the click analytics.
    """
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection error.")

    try:
        cursor = conn.cursor()
        
        # 1. Look up the short code
        cursor.execute(
            "SELECT id, original_url FROM links WHERE short_code = ?",
            (short_code,)
        )
        link = cursor.fetchone()
        
        if not link:
            raise HTTPException(status_code=404, detail="Short URL not found.")

        link_id = link["id"]
        original_url = link["original_url"]

        # 2. Log the click analytics (raw SQL)
        ip_address = request.client.host
        user_agent = request.headers.get("user-agent")
        
        cursor.execute(
            "INSERT INTO clicks (link_id, ip_address, user_agent) VALUES (?, ?, ?)",
            (link_id, ip_address, user_agent)
        )
        conn.commit()

        # 3. Redirect to destination
        return RedirectResponse(url=original_url, status_code=302)

    except sqlite3.Error as e:
        logging.error(f"Database error during redirect: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")
    finally:
        conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
