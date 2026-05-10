import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Text, Float, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class AnalyticsEvent(Base):
    __tablename__ = "analytics_events"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=True)
    product_id: Mapped[str] = mapped_column(String, ForeignKey("products.id"), nullable=True)

    event_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    channel: Mapped[str] = mapped_column(String(100), nullable=True)
    source: Mapped[str] = mapped_column(String(255), nullable=True)
    session_id: Mapped[str] = mapped_column(String(255), nullable=True)
    visitor_id: Mapped[str] = mapped_column(String(255), nullable=True)

    event_data: Mapped[str] = mapped_column(JSON, nullable=True)
    extra_data: Mapped[str] = mapped_column("metadata", JSON, nullable=True)

    ip_address: Mapped[str] = mapped_column(String(50), nullable=True)
    user_agent: Mapped[str] = mapped_column(String(500), nullable=True)
    referrer: Mapped[str] = mapped_column(String(1000), nullable=True)

    value: Mapped[float] = mapped_column(Float, default=0.0)
    currency: Mapped[str] = mapped_column(String(10), default="USD")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True
    )


class SalesRecord(Base):
    __tablename__ = "sales_records"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False)
    product_id: Mapped[str] = mapped_column(String, ForeignKey("products.id"), nullable=False)

    gumroad_sale_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=True)
    gumroad_purchase_id: Mapped[str] = mapped_column(String(255), nullable=True)

    customer_email: Mapped[str] = mapped_column(String(255), nullable=True)
    customer_name: Mapped[str] = mapped_column(String(255), nullable=True)

    amount: Mapped[float] = mapped_column(Float, nullable=False)
    gumroad_fee: Mapped[float] = mapped_column(Float, default=0.0)
    net_amount: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="USD")

    quantity: Mapped[int] = mapped_column(Integer, default=1)
    license_key: Mapped[str] = mapped_column(String(255), nullable=True)

    sale_source: Mapped[str] = mapped_column(String(255), nullable=True)
    affiliate: Mapped[str] = mapped_column(String(255), nullable=True)
    coupon_used: Mapped[str] = mapped_column(String(255), nullable=True)

    refunded: Mapped[bool] = mapped_column(default=False)
    refunded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    disputed: Mapped[bool] = mapped_column(default=False)

    gumroad_data: Mapped[str] = mapped_column(JSON, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True
    )
