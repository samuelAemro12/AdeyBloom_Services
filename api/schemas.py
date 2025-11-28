from typing import List, Optional
from pydantic import BaseModel


class ProductListItem(BaseModel):
    id: Optional[str]
    name: Optional[str]
    price: Optional[float]
    currency: Optional[str]
    image: Optional[str]
    stock: Optional[int]
    active: Optional[bool]


class ProductDetail(ProductListItem):
    description: Optional[str]
    images: List[str] = []
    brand: Optional[str]
    category: Optional[str]


class DBStatus(BaseModel):
    connected: bool
    product_count: Optional[int] = None
