## Author
**James Jnr Iorkuah**

## Project Name
**IT Asset Register**

## Description
A web application for recording and tracking IT assets such as laptops, routers, printers, and monitors. Each asset includes a tag, type, model, status, and is stored in a persistent SQLite database using SQLAlchemy.

## Stack
- **Backend Framework:** FastAPI (Python)
- **Database:** SQLite with SQLAlchemy ORM
- **ASGI Server:** Uvicorn
- **Templating Engine:** Jinja2
- **Styling:** CSS3
- **Version Control:** Git and GitHub

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/Jamesiorkusah/asset-register.git
   cd asset-register
   ```

2. Activate the virtual environment:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   or on macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create the database tables and seed initial sample data (first-time setup):
   ```bash
   python seed.py
   ```

5. Start the development server:
   ```bash
   uvicorn main:app --reload
   ```

6. Open the app in a browser:
   - API message: http://127.0.0.1:8000
   - Assets page: http://127.0.0.1:8000/assets

## Database Notes
This project now uses SQLite for persistent storage via SQLAlchemy. The database file is created automatically when the app runs, and `seed.py` adds initial asset records the first time you set up the project.

## Progress
### Week 1
- Cloned and initialized the Git repository.
- Set up the project structure and virtual environment.
- Built the FastAPI foundation and template structure.

### Week 2
- Added asset creation forms and database-backed storage.
- Implemented filtering and searching for assets.
- Replaced the temporary in-memory list with a persistent SQLite database using SQLAlchemy.
- Added `seed.py` for first-time setup and initial data seeding.

### Week 3
- Fixed route registration and database-backed asset detail rendering.
- Added persistent SQLite storage for asset records across app restarts.
- Resolved duplicate-tag checks by querying the database instead of the old in-memory list.
- Improved template and static file setup so pages render consistently in the browser.
- Verified the app can save assets and keep them available after restarting the server.

### Week 4
- Completed full CRUD for assets: create, view details, edit, and delete records.
- Added duplicate-tag checks when creating or updating assets.
- Added HTMX live search by asset tag or model, updating the asset rows without a full page reload.
- Kept status filtering available alongside search.
