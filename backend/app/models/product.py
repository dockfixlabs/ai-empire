import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Text, Float, Boolean, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False)
    gumroad_product_id: Mapped[str] = mapped_column(String(255), nullable=True)

    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    rich_description: Mapped[str] = mapped_column(Text, nullable=True)
    short_description: Mapped[str] = mapped_column(String(300), nullable=True)

    price: Mapped[float] = mapped_column(Float, default=9.99)
    original_price: Mapped[float] = mapped_column(Float, nullable=True)
    currency: Mapped[str] = mapped_column(String(10), default="USD")

    category: Mapped[str] = mapped_column(String(100), nullable=True)
    tags: Mapped[str] = mapped_column(Text, nullable=True)
    keywords: Mapped[str] = mapped_column(Text, nullable=True)

    file_url: Mapped[str] = mapped_column(String(1000), nullable=True)
    preview_url: Mapped[str] = mapped_column(String(1000), nullable=True)
    cover_image_url: Mapped[str] = mapped_column(String(1000), nullable=True)
    thumbnail_url: Mapped[str] = mapped_column(String(1000), nullable=True)

    content_type: Mapped[str] = mapped_column(String(50), default="pdf")
    file_size_mb: Mapped[float] = mapped_column(Float, nullable=True)
    pages_count: Mapped[int] = mapped_column(Integer, nullable=True)

    sales_count: Mapped[int] = mapped_column(Integer, default=0)
    revenue: Mapped[float] = mapped_column(Float, default=0.0)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    review_count: Mapped[int] = mapped_column(Integer, default=0)

    is_published: Mapped[bool] = mapped_column(Boolean, default=False)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[str] = mapped_column(String(50), default="draft")

    gumroad_data: Mapped[str] = mapped_column(JSON, nullable=True)
    seo_data: Mapped[str] = mapped_column(JSON, nullable=True)
    market_research_data: Mapped[str] = mapped_column(JSON, nullable=True)

    ai_generated: Mapped[bool] = mapped_column(Boolean, default=False)
    generation_prompt: Mapped[str] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    owner = relationship("User", back_populates="products")
    variants = relationship("ProductVariant", back_populates="product", cascade="all, delete-orphan")


class ProductVariant(Base):
    __tablename__ = "product_variants"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id: Mapped[str] = mapped_column(String, ForeignKey("products.id"), nullable=False)
    gumroad_variant_id: Mapped[str] = mapped_column(String(255), nullable=True)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    file_url: Mapped[str] = mapped_column(String(1000), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    product = relationship("Product", back_populates="variants")
