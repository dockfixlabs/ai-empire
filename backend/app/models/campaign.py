import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Text, Float, Boolean, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Campaign(Base):
    __tablename__ = "campaigns"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False)
    product_id: Mapped[str] = mapped_column(String, ForeignKey("products.id"), nullable=True)

    name: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    campaign_type: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="draft")

    target_audience: Mapped[str] = mapped_column(Text, nullable=True)
    target_psychographics: Mapped[str] = mapped_column(JSON, nullable=True)
    value_proposition: Mapped[str] = mapped_column(Text, nullable=True)
    hooks: Mapped[str] = mapped_column(JSON, nullable=True)
    key_messages: Mapped[str] = mapped_column(JSON, nullable=True)

    budget: Mapped[float] = mapped_column(Float, default=0.0)
    total_spent: Mapped[float] = mapped_column(Float, default=0.0)
    total_revenue: Mapped[float] = mapped_column(Float, default=0.0)
    total_clicks: Mapped[int] = mapped_column(Integer, default=0)
    total_conversions: Mapped[int] = mapped_column(Integer, default=0)
    total_impressions: Mapped[int] = mapped_column(Integer, default=0)

    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    launch_wave: Mapped[int] = mapped_column(Integer, default=1)
    is_automated: Mapped[bool] = mapped_column(Boolean, default=True)
    ai_optimized: Mapped[bool] = mapped_column(Boolean, default=True)

    viral_score: Mapped[float] = mapped_column(Float, default=0.0)
    engagement_score: Mapped[float] = mapped_column(Float, default=0.0)
    conversion_rate: Mapped[float] = mapped_column(Float, default=0.0)

    strategy_data: Mapped[str] = mapped_column(JSON, nullable=True)
    performance_data: Mapped[str] = mapped_column(JSON, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
    launched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    owner = relationship("User", back_populates="campaigns")
    channels = relationship("CampaignChannel", back_populates="campaign", cascade="all, delete-orphan")
    results = relationship("CampaignResult", back_populates="campaign", cascade="all, delete-orphan")


class CampaignChannel(Base):
    __tablename__ = "campaign_channels"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    campaign_id: Mapped[str] = mapped_column(String, ForeignKey("campaigns.id"), nullable=False)

    channel: Mapped[str] = mapped_column(String(100), nullable=False)
    channel_type: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending")
    content: Mapped[str] = mapped_column(Text, nullable=True)
    content_assets: Mapped[str] = mapped_column(JSON, nullable=True)
    scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    posted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    post_url: Mapped[str] = mapped_column(String(1000), nullable=True)
    engagement_metrics: Mapped[str] = mapped_column(JSON, nullable=True)
    error_message: Mapped[str] = mapped_column(Text, nullable=True)
    retry_count: Mapped[int] = mapped_column(Integer, default=0)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    campaign = relationship("Campaign", back_populates="channels")


class CampaignResult(Base):
    __tablename__ = "campaign_results"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    campaign_id: Mapped[str] = mapped_column(String, ForeignKey("campaigns.id"), nullable=False)

    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    channel: Mapped[str] = mapped_column(String(100), nullable=True)
    impressions: Mapped[int] = mapped_column(Integer, default=0)
    clicks: Mapped[int] = mapped_column(Integer, default=0)
    conversions: Mapped[int] = mapped_column(Integer, default=0)
    revenue: Mapped[float] = mapped_column(Float, default=0.0)
    spend: Mapped[float] = mapped_column(Float, default=0.0)
    engagement_rate: Mapped[float] = mapped_column(Float, default=0.0)
    extra_data: Mapped[str] = mapped_column("metadata", JSON, nullable=True)

    campaign = relationship("Campaign", back_populates="results")
