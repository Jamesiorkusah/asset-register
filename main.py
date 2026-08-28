from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

# FastAPI creates the web application and provides the tools for defining routes.
app = FastAPI()

# Jinja2Templates lets Python send data to HTML files with dynamic content.
# The folder contains the HTML templates used by the /assets page.
templates = Jinja2Templates(directory="templates")

# This is temporary in-memory data: it resets whenever the application restarts.
# Each dictionary represents one asset and stores its tag, type, model, and status.
assets = [
    {"tag": "NIT-001", "type": "laptop", "model": "Dell XPS 13", "status": "in use"},
    {"tag": "NIT-002", "type": "router", "model": "Mikrotik hEX", "status": "in use"},
    {"tag": "NIT-003", "type": "printer", "model": "HP LaserJet Pro", "status": "faulty"},
]

# @app.get("/") connects this function to GET requests sent to the website root.
# A GET request is normally used when a user wants to read or retrieve data.
@app.get("/")
def home():
    # FastAPI automatically converts this Python dictionary into a JSON response.
    return {"message": "Asset Register is running!"}

# This route displays all assets in a browser-friendly HTML page.
@app.get("/assets", response_class=HTMLResponse)
def list_assets(request: Request):
    # The request must be passed to the template so Jinja can create the response.
    # The assets list is also passed in, allowing assets.html to display each item.
    return templates.TemplateResponse(
        "assets.html", {"request": request, "assets": assets}
    )

# The {tag} part is a URL parameter. For example, /assets/NIT-001 looks up NIT-001.
@app.get("/assets/{tag}")
def get_asset_by_tag(tag: str):
    # Check each asset until the tag from the URL matches an asset's tag.
    for asset in assets:
        if asset["tag"] == tag:
            # Return the matching asset as JSON and stop searching.
            return {"asset": asset}

    # This response is returned only when no asset has the requested tag.
    return {"error": "Asset not found"}

# Run Uvicorn only when this file is started directly, not when it is imported.
if __name__ == "__main__":
    # reload=True restarts the development server automatically after code changes.
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
