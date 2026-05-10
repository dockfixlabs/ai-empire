from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.user import User
from app.dependencies import get_current_user
from app.schemas.marketing import MarketResearchRequest, MarketOpportunity, AgentTaskRequest, AgentTaskResponse
from agents.orchestrator import AgentOrchestrator
from agents.marketing.market_research import MarketResearchAgent
from agents.marketing.viral_engine import ViralEngine
from agents.marketing.content_strategy import ContentStrategyAgent
from agents.marketing.launch_controller import LaunchController
import uuid
from datetime import datetime, timezone

router = APIRouter(prefix="/agents", tags=["AI Agents"])


@router.post("/research", response_model=MarketOpportunity)
async def research_market(
    request: MarketResearchRequest,
    user: User = Depends(get_current_user),
):
    agent = MarketResearchAgent(user_id=user.id)
    result = await agent.research(
        niche=request.niche,
        keywords=request.keywords,
        target_audience=request.target_audience,
        content_type=request.content_type,
    )
    return result


@router.post("/generate-strategy")
async def generate_strategy(
    product_id: str,
    user: User = Depends(get_current_user),
):
    orchestrator = AgentOrchestrator(user_id=user.id)
    strategy = await orchestrator.create_go_to_market_strategy(product_id)
    return strategy


@router.post("/execute-campaign/{campaign_id}")
async def execute_campaign(
    campaign_id: str,
    user: User = Depends(get_current_user),
):
    orchestrator = AgentOrchestrator(user_id=user.id)
    result = await orchestrator.execute_campaign(campaign_id)
    return result


@router.post("/viral-content")
async def generate_viral_content(
    product_id: str,
    platform: str = "twitter",
    user: User = Depends(get_current_user),
):
    engine = ViralEngine(user_id=user.id)
    content = await engine.generate_viral_content(product_id, platform)
    return content


@router.post("/launch-plan")
async def create_launch_plan(
    product_id: str,
    user: User = Depends(get_current_user),
):
    controller = LaunchController(user_id=user.id)
    plan = await controller.create_multi_wave_launch(product_id)
    return plan


@router.post("/task", response_model=AgentTaskResponse)
async def submit_task(
    request: AgentTaskRequest,
    background_tasks: BackgroundTasks,
    user: User = Depends(get_current_user),
):
    orchestrator = AgentOrchestrator(user_id=user.id)
    task_id = str(uuid.uuid4())

    background_tasks.add_task(
        orchestrator.process_task,
        task_id=task_id,
        agent_type=request.agent_type,
        task=request.task,
        context=request.context,
    )

    return AgentTaskResponse(
        task_id=task_id,
        agent_type=request.agent_type,
        status="queued",
        created_at=datetime.now(timezone.utc),
    )
