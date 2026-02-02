# Project Context: LinkSwift Deployment

## 1. Goal
Deploy the URL Shortener (LinkSwift) to Render.com with persistent storage.

## 2. Infrastructure Requirements
- **Hosting:** Render.com (Web Service).
- **Storage:** Render Persistent Disk (1GB) for SQLite.
- **Repository:** GitHub.

## 3. Final Adjustments
- Database path must support `/data/` mount point for production.
- Environment variables for Port handling ($PORT).