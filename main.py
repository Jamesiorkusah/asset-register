from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional
import uvicorn

import models
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static/static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/")
def home():
    return {"message": "Asset Register is running!"}


@app.get("/assets", response_class=HTMLResponse)
def list_assets_page(
    request: Request,
    status: Optional[str] = None,
    q: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Asset)
    if status:
        query = query.filter(models.Asset.status == status)
    if q:
        pattern = f"%{q}%"
        query = query.filter(
            models.Asset.model.ilike(pattern) | models.Asset.tag.ilike(pattern)
        )
    results = query.order_by(models.Asset.tag).all()
    return templates.TemplateResponse(
        request,
        "assets.html",
        {"request": request, "assets": results, "status": status, "q": q},
    )


@app.get("/assets/new", response_class=HTMLResponse)
def new_asset_form(request: Request):
    return templates.TemplateResponse(request, "assets_form.html", {"request": request})


@app.get("/assets/{tag}", response_class=HTMLResponse)
def get_asset(tag: str, request: Request, db: Session = Depends(get_db)):
    asset = db.query(models.Asset).filter(models.Asset.tag == tag).first()
    if not asset:
        return HTMLResponse(f"Asset {tag} not found", status_code=404)
    return templates.TemplateResponse(
        request,
        "asset_detail.html",
        {"request": request, "asset": asset},
    )
@app.get("/assets/{asset_id}/edit", response_class=HTMLResponse)
def edit_asset_form(asset_id: int, request: Request, db: Session = Depends(get_db)):
    asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
    if not asset:
        return HTMLResponse("Asset not found", status_code=404)
    return templates.TemplateResponse(
        request,
        "asset_edit.html",
        {"request": request, "asset": asset},
    )


@app.post("/assets/new")
def create_asset(
    tag: str = Form(...),
    asset_type: str = Form(...),
    model: str = Form(...),
    status: str = Form(...),
    db: Session = Depends(get_db),
):
    existing = db.query(models.Asset).filter(models.Asset.tag == tag).first()
    if existing:
        return RedirectResponse(url="/assets?error=duplicate", status_code=303)

    new_asset = models.Asset(tag=tag, type=asset_type, model=model, status=status)
    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)
    return RedirectResponse(url="/assets", status_code=303)

@app.post("/assets/{asset_id}/edit")
def update_asset(
    asset_id: int,
    tag: str = Form(...),
    asset_type: str = Form(...),
    model: str = Form(...),
    status: str = Form(...),
    db: Session = Depends(get_db),
):
    asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
    if not asset:
        return HTMLResponse("Asset not found", status_code=404)
    clash = db.query(models.Asset).filter(
        models.Asset.tag == tag, models.Asset.id != asset_id
    ).first()
    if clash:
        return RedirectResponse(url=f"/assets/{asset_id}/edit?error=duplicate",
                                status_code=303)
    asset.tag = tag
    asset.type = asset_type
    asset.model = model
    asset.status = status
    db.commit()
    return RedirectResponse(url="/assets", status_code=303)


@app.post("/assets/{asset_id}/delete", response_class=HTMLResponse)
def delete_asset(asset_id: int, request: Request, db: Session = Depends(get_db)):
    asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
    if asset:
        db.delete(asset)
        db.commit()
    remaining = db.query(models.Asset).order_by(models.Asset.tag).all()
    return templates.TemplateResponse(
        request,
        "templates/_asset_rows.html",
        {"request": request, "assets": remaining},
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)