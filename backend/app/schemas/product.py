from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ProductCreate(BaseModel):
    title: str
    description: Optional[str] = None
    price: float = 9.99
    category: Optional[str] = None
    tags: Optional[str] = None
    content_type: str = "pdf"
    ai_generated: bool = False
    generation_prompt: Optional[str] = None


class ProductUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    tags: Optional[str] = None
    is_published: Optional[bool] = None


class ProductResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    short_description: Optional[str] = None
    price: float
    original_price: Optional[float] = None
    currency: str
    category: Optional[str] = None
    tags: Optional[str] = None
    content_type: str
    cover_image_url: Optional[str] = None
    sales_count: int
    revenue: float
    rating: Optional[float] = None
    is_published: bool
    status: str
    gumroad_product_id: Optional[str] = None
    ai_generated: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    products: List[ProductResponse]
    total: int
    page: int
    page_size: int
