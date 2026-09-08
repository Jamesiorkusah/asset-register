
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
import uvicorn

# FastAPI creates the web app and handles HTTP requests.
# In a presentation, this is the main backend framework we are using.
app = FastAPI()

# Jinja2Templates connects Python data to HTML files.
# This allows the app to pass asset information into the templates in templates/.
templates = Jinja2Templates(directory="templates")

# In-memory data store: this is temporary storage that resets when the server restarts.
# Each dictionary stores one asset record: tag, type, and status.
assets = [
    {"tag": "NIT-001", "type": "laptop", "status": "in use"},
    {"tag": "NIT-002", "type": "router", "status": "in use"},
    {"tag": "NIT-003", "type": "printer", "status": "faulty"},
]


# Route flow explanation:
# 1. The browser sends an HTTP request.
# 2. FastAPI matches the URL to a function here.
# 3. The function performs logic and returns data or a redirect.
# 4. The browser receives the response and displays it.


# This is the home route: GET /
# It is a simple example of returning JSON using FastAPI.
@app.get("/")
def home():
    # FastAPI automatically converts Python dictionaries into JSON responses.
    # This is useful for APIs and quick testing in the browser.
    return {"message": "Asset Register is running!"}


# This route shows all assets in an HTML page.
# Query parameters like ?status=in%20use or ?q=router can be used for filters.
@app.get("/assets", response_class=HTMLResponse)
def list_assets(request: Request, status: Optional[str] = None, q: Optional[str] = None):
    # Start with the full list, then narrow it down if filters are provided.
    results = assets

    # Example: /assets?status=in%20use
    # This filters the list to only assets with that exact status.
    if status:
        results = [asset for asset in results if asset["status"].lower() == status.lower()]

    # Example: /assets?q=router
    # This searches the tag and type fields for the search term.
    if q:
        term = q.lower()
        results = [
            asset
            for asset in results
            if term in asset["tag"].lower() or term in asset["type"].lower()
        ]

    # TemplateResponse sends the filtered list to assets.html for display in the browser.
    return templates.TemplateResponse(
        "assets.html",
        {"request": request, "assets": results, "status": status, "q": q},
    )


# This route shows a form that lets the user create a new asset.
@app.get("/assets/new", response_class=HTMLResponse)
def new_asset_form(request: Request):
    # The form page is rendered with Jinja2 so the HTML can display fields.
    return templates.TemplateResponse(request, "assets_form.html", {"request": request})


# This route gets one asset using a URL parameter.
# Example: /assets/NIT-001
@app.get("/assets/{tag}")
def get_asset_by_tag(tag: str):
    # Loop through the list and compare each asset tag to the value in the URL.
    for asset in assets:
        if asset["tag"] == tag:
            # If a match is found, return just that asset as JSON.
            return {"asset": asset}

    # If nothing matches, return an error message.
    return {"error": "Asset not found"}


# This route receives form data when the user submits the "new asset" form.
@app.post("/assets/new")
def create_asset(
    tag: str = Form(...),
    asset_type: str = Form(...),
    status: str = Form(...),
):
    # Step 1: prevent duplicate asset tags.
    # This keeps the data clean and avoids confusion in the register.
    for existing in assets:
        if existing["tag"].lower() == tag.lower():
            return RedirectResponse(url="/assets?error=duplicate", status_code=303)

    # Step 2: build a new asset record from the submitted form values.
    new_asset = {
        "tag": tag,
        "type": asset_type,
        "status": status,
    }

    # Step 3: store the record in the temporary in-memory list.
    assets.append(new_asset)
    print("RECEIVED:", new_asset)

    # Step 4: redirect the user back to the asset list page.
    return RedirectResponse(url="/assets", status_code=303)


# This block runs only when the file is executed directly.
# It starts the local web server so the app can be viewed in the browser.
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)