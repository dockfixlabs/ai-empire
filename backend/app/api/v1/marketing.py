from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.user import User
from app.models.campaign import Campaign
from app.schemas.marketing import CampaignCreate, CampaignResponse
from app.dependencies import get_current_user

router = APIRouter(prefix="/marketing", tags=["Marketing"])


@router.get("/campaigns", response_model=list[CampaignResponse])
async def list_campaigns(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Campaign).where(Campaign.user_id == user.id).order_by(Campaign.created_at.desc())
    )
    campaigns = result.scalars().all()
    return [CampaignResponse.model_validate(c) for c in campaigns]


@router.post("/campaigns", response_model=CampaignResponse, status_code=201)
async def create_campaign(
    data: CampaignCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    campaign = Campaign(
        user_id=user.id,
        product_id=data.product_id,
        name=data.name,
        campaign_type=data.campaign_type,
        target_audience=data.target_audience,
        budget=data.budget,
        start_date=data.start_date,
        end_date=data.end_date,
    )
    db.add(campaign)
    await db.flush()
    return CampaignResponse.model_validate(campaign)


@router.get("/campaigns/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(
    campaign_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Campaign).where(Campaign.id == campaign_id, Campaign.user_id == user.id)
    )
    campaign = result.scalar_one_or_none()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return CampaignResponse.model_validate(campaign)


@router.post("/campaigns/{campaign_id}/launch", response_model=CampaignResponse)
async def launch_campaign(
    campaign_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Campaign).where(Campaign.id == campaign_id, Campaign.user_id == user.id)
    )
    campaign = result.scalar_one_or_none()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    from datetime import datetime, timezone
    campaign.status = "launching"
    campaign.launched_at = datetime.now(timezone.utc)
    await db.flush()

    return CampaignResponse.model_validate(campaign)
