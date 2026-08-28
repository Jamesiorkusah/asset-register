from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home():
    return {"message": "Asset Register is running!"}  

@app.get("/assets", response_class=HTMLResponse)
def list_assets(request: Request):
    return templates.TemplateResponse(
        "assets.html", {"request": request, "assets": assets}
    )

@app.get("/assets/{tag}")
def get_asset_by_tag(tag: str):
    for asset in assets:
        if asset["tag"] == tag:
            return {"asset": asset}
    return {"error": "Asset not found"}

assets = [
    { "tag": "NIT-001", "type": "laptop", "model": "Dell XPS 13", "status": "in use" },
    { "tag": "NIT-002", "type": "router", "model": "Mikrotik hEX", "status": "in use" },
    { "tag": "NIT-003", "type": "printer", "model": "HP LaserJet Pro", "status": "faulty" },
]

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
