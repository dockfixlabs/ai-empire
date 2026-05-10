"""Automatic Agent Scheduler - cron-like periodic agent execution"""
import asyncio
from datetime import datetime, timezone
from typing import Dict, Optional
from sqlalchemy import select
from app.core.database import get_session_factory
from app.models.user import User
from app.models.activity import AgentSession, AgentActivity
from app.api.v1.agent_control import broadcast_activity
from app.services.innovation.engine import InnovationMarketingEngine

SCHEDULE_CONFIG: Dict[str, dict] = {}

_running = False


async def run_scheduled_agent(agent_name: str, user: User):
    """Run a single scheduled agent - uses isolated sessions for all DB writes"""
    factory = get_session_factory()

    # Log start
    async with factory() as db:
        try:
            activity = AgentActivity(
                user_id=user.id,
                agent_name=f"scheduler_{agent_name}",
                action=f"Scheduled run: {agent_name}",
                status="running",
            )
            db.add(activity)
            await db.commit()

            await broadcast_activity({
                "type": "scheduler_started",
                "agent_name": agent_name,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "activity_id": activity.id,
            })
        except Exception as e:
            print(f"[Scheduler] Log start error: {e}")

    # Run the agent engine (no DB session held during AI call)
    try:
        engine = InnovationMarketingEngine(user_id=user.id)
        product = {"name": "Gumroad Product", "price": 29.99, "description": "Digital product"}
        channel_map = {
            "market_research": "market_research",
            "seo_empire": "seo_empire",
            "email_3d": "email_3d",
        }
        channel = channel_map.get(agent_name)
        if channel and channel in engine.engines:
            await engine.execute_channel(channel, product)
    except Exception as e:
        print(f"[Scheduler] Agent execution error: {e}")

    # Update session stats
    async with factory() as db:
        try:
            result = await db.execute(
                select(AgentSession).where(
                    AgentSession.user_id == user.id,
                    AgentSession.agent_name == agent_name,
                )
            )
            session = result.scalar_one_or_none()
            if session:
                session.total_runs = (session.total_runs or 0) + 1
            await db.commit()
        except Exception as e:
            print(f"[Scheduler] Session update error: {e}")


async def scheduler_loop():
    """Main scheduler loop - runs every 60 seconds checking for due tasks"""
    global _running
    _running = True
    last_run: Dict[str, datetime] = {}

    while _running:
        try:
            factory = get_session_factory()
            users = []
            async with factory() as db:
                result = await db.execute(select(User).where(User.is_active == True))
                users = result.scalars().all()

            now = datetime.now(timezone.utc)
            for user in users:
                for agent_name, config in SCHEDULE_CONFIG.items():
                    key = f"{user.id}:{agent_name}"
                    last = last_run.get(key)
                    if last is None or (now - last).total_seconds() >= config["interval_hours"] * 3600:
                        last_run[key] = now
                        asyncio.create_task(run_scheduled_agent(agent_name, user))
        except Exception as e:
            print(f"[Scheduler] Loop error: {e}")

        for _ in range(60):
            if not _running:
                break
            await asyncio.sleep(1)


def start_scheduler():
    """Start the background scheduler task"""
    loop = asyncio.get_running_loop()
    task = loop.create_task(scheduler_loop())
    print("[Scheduler] Started background scheduler")
    return task


def stop_scheduler():
    """Stop the background scheduler"""
    global _running
    _running = False
    print("[Scheduler] Stopped background scheduler")
