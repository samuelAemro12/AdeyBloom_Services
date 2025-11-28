from fastapi import APIRouter, HTTPException, Request
from typing import Optional

from . import services
from . import schemas

router = APIRouter()


@router.get("/products", response_model=list[schemas.ProductListItem])
async def list_products(request: Request, limit: int = 10, skip: int = 0, q: Optional[str] = None, category: Optional[str] = None):
    if limit < 1:
        raise HTTPException(status_code=400, detail="limit must be >= 1")
    if limit > 50:
        limit = 50
    filters = {"active": True}
    if q:
        # simple text search on name (case-insensitive)
        filters["name"] = {"$regex": q, "$options": "i"}
    if category:
        filters["category"] = category
    db = request.app.state.db
    products = await services.get_products(db, limit=limit, skip=skip, filters=filters)
    return products


@router.get("/products/{product_id}", response_model=schemas.ProductDetail)
async def get_product(request: Request, product_id: str):
    db = request.app.state.db
    product = await services.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("/db/status", response_model=schemas.DBStatus)
async def db_status(request: Request):
    db = request.app.state.db
    connected = db is not None
    product_count = None
    if connected:
        try:
            product_count = await db["products"].count_documents({})
        except Exception:
            product_count = None
    return {"connected": connected, "product_count": product_count}
