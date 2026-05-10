"""Innovation Marketing API endpoints"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.dependencies import get_current_user
from app.core.database import get_db
from app.services.innovation.engine import InnovationMarketingEngine
from app.core.config import get_settings

router = APIRouter(prefix="/marketing", tags=["Innovation Marketing"])
settings = get_settings()


def _get_engine(user: User, db: AsyncSession) -> InnovationMarketingEngine:
    return InnovationMarketingEngine(user_id=user.id, db=db, user=user)


@router.post("/master-plan")
async def create_master_plan(
    data: dict,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create complete integrated marketing master plan"""
    engine = _get_engine(user, db)
    plan = await engine.create_master_plan(data.get("product", {}))
    return plan


@router.post("/channel/{channel}")
async def execute_channel(
    channel: str,
    data: dict,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Execute a specific marketing channel"""
    valid = ["email_3d", "seo_empire", "launch", "viral_referral", "interactive", "partnership", "community_flywheel"]
    if channel not in valid:
        raise HTTPException(400, f"Invalid channel. Valid: {valid}")
    engine = _get_engine(user, db)
    result = await engine.execute_channel(channel, data.get("product", {}), data.get("phase", 1))
    return {"channel": channel, "result": result}


@router.post("/launch-plan")
async def create_launch_plan(
    data: dict,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create comprehensive launch plan"""
    engine = _get_engine(user, db)
    plan = await engine.execute_channel("launch", data.get("product", {}))
    plan["timeline"] = await engine._build_timeline({})
    return {"plan": plan, "product": data.get("product", {}).get("name")}


@router.post("/email-campaign")
async def create_email_campaign(
    data: dict,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create deep email campaign strategy"""
    engine = _get_engine(user, db)
    result = await engine.execute_channel("email_3d", data.get("product", {}))
    return result


@router.post("/seo-strategy")
async def create_seo_strategy(
    data: dict,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create SEO content empire strategy"""
    engine = _get_engine(user, db)
    result = await engine.execute_channel("seo_empire", data.get("product", {}))
    return result


@router.post("/referral-program")
async def create_referral_program(
    data: dict,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create viral referral program"""
    engine = _get_engine(user, db)
    result = await engine.execute_channel("viral_referral", data.get("product", {}))
    return result


@router.post("/interactive-content")
async def create_interactive_content(
    data: dict,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create interactive content assets"""
    engine = _get_engine(user, db)
    result = await engine.execute_channel("interactive", data.get("product", {}))
    return result


@router.post("/partnerships")
async def find_partnerships(
    data: dict,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Find and manage partnerships"""
    engine = _get_engine(user, db)
    result = await engine.execute_channel("partnership", data.get("product", {}))
    return result


@router.post("/community")
async def build_community(
    data: dict,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Build community flywheel"""
    engine = _get_engine(user, db)
    result = await engine.execute_channel("community_flywheel", data.get("product", {}))
    return result
