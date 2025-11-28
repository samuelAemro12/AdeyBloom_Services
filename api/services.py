from typing import List, Optional, Dict, Any
from bson import ObjectId


def _doc_to_product_list_item(doc: Dict[str, Any]) -> Dict[str, Any]:
    if not doc:
        return {}
    return {
        "id": str(doc.get("_id")) if doc.get("_id") else None,
        "name": doc.get("name"),
        "price": doc.get("price"),
        "currency": doc.get("currency"),
        "image": (doc.get("images") or [None])[0] if doc.get("images") else None,
        "stock": doc.get("stock"),
        "active": doc.get("active", True),
    }


def _doc_to_product_detail(doc: Dict[str, Any]) -> Dict[str, Any]:
    if not doc:
        return {}
    return {
        "id": str(doc.get("_id")) if doc.get("_id") else None,
        "name": doc.get("name"),
        "description": doc.get("description"),
        "price": doc.get("price"),
        "currency": doc.get("currency"),
        "images": doc.get("images") or [],
        "stock": doc.get("stock"),
        "active": doc.get("active", True),
        "brand": doc.get("brand"),
        "category": str(doc.get("category")) if doc.get("category") else None,
    }


async def get_products(db, limit: int = 10, skip: int = 0, filters: Optional[Dict] = None) -> List[Dict[str, Any]]:
    """Return a list of products from the `products` collection.

    `filters` should be a MongoDB query dict. This function projects a small set
    of fields suitable for list views.
    """
    if db is None:
        return []
    query = filters or {"active": True}
    projection = {"name": 1, "price": 1, "currency": 1, "images": 1, "stock": 1, "active": 1}
    cursor = db["products"].find(query, projection)
    docs = await cursor.skip(skip).limit(limit).to_list(length=limit)
    return [_doc_to_product_list_item(d) for d in docs]


async def get_product_by_id(db, id: str) -> Optional[Dict[str, Any]]:
    if db is None:
        return None
    try:
        oid = ObjectId(id)
    except Exception:
        return None
    doc = await db["products"].find_one({"_id": oid})
    if not doc:
        return None
    return _doc_to_product_detail(doc)
