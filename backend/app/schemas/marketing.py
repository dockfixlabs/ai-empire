from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class CampaignCreate(BaseModel):
    name: str
    product_id: Optional[str] = None
    campaign_type: str = "multi_channel"
    target_audience: Optional[str] = None
    budget: float = 0.0
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    channels: Optional[List[str]] = None


class CampaignResponse(BaseModel):
    id: str
    name: str
    campaign_type: str
    status: str
    total_spent: float
    total_revenue: float
    total_clicks: int
    total_conversions: int
    total_impressions: int
    conversion_rate: float
    viral_score: float
    engagement_score: float
    is_automated: bool
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class MarketResearchRequest(BaseModel):
    niche: Optional[str] = None
    keywords: Optional[List[str]] = None
    target_audience: Optional[str] = None
    budget_range: Optional[str] = None
    content_type: Optional[str] = None


class MarketOpportunity(BaseModel):
    product_idea: str
    description: str
    target_audience: str
    estimated_demand: str
    competition_level: str
    suggested_price: float
    recommended_format: str
    keywords: List[str]
    angle: str
    pain_points: List[str]
    unique_value: str
    viral_potential: str
    confidence_score: float


class MarketingStrategy(BaseModel):
    campaign_name: str
    overall_strategy: str
    target_psychographic: Dict[str, Any]
    hooks: List[str]
    channels: List[Dict[str, Any]]
    content_plan: List[Dict[str, Any]]
    viral_mechanisms: List[str]
    scarcity_tactics: List[str]
    social_proof_plan: List[str]
    referral_incentives: List[str]
    timeline: Dict[str, Any]
    kpis: Dict[str, float]
    budget_allocation: Dict[str, float]


class ContentPiece(BaseModel):
    channel: str
    content_type: str
    content: str
    visual_description: Optional[str] = None
    best_time_to_post: Optional[str] = None
    hashtags: Optional[List[str]] = None
    call_to_action: str


class ViralContentBrief(BaseModel):
    hook: str
    story_angle: str
    emotional_triggers: List[str]
    format: str
    platform: str
    predicted_viral_score: float


class AgentTaskRequest(BaseModel):
    agent_type: str
    task: str
    context: Optional[Dict[str, Any]] = None
    priority: int = 0


class AgentTaskResponse(BaseModel):
    task_id: str
    agent_type: str
    status: str
    result: Optional[Dict[str, Any]] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
