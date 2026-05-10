import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Boolean, DateTime, Text, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=True)
    avatar_url: Mapped[str] = mapped_column(String(500), nullable=True)

    gumroad_token: Mapped[str] = mapped_column(String(500), nullable=True)
    gumroad_refresh_token: Mapped[str] = mapped_column(String(500), nullable=True)

    openai_api_key: Mapped[str] = mapped_column(String(500), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    subscription_tier: Mapped[str] = mapped_column(String(50), default="free")

    total_revenue: Mapped[float] = mapped_column(Float, default=0.0)
    total_products: Mapped[int] = mapped_column(default=0)
    total_sales: Mapped[int] = mapped_column(default=0)

    preferences: Mapped[str] = mapped_column("preferences_json", Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    products = relationship("Product", back_populates="owner", cascade="all, delete-orphan")
    campaigns = relationship("Campaign", back_populates="owner", cascade="all, delete-orphan")
