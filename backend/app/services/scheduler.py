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
from app.services.multi_ai import MultiAIService

SCHEDULE_CONFIG: Dict[str, dict] = {
    "market_research": {"interval_hours": 1, "label": "أبحاث السوق"},
    "email_3d": {"interval_hours": 2, "label": "Email 3D"},
    "seo_empire": {"interval_hours": 3, "label": "SEO Empire"},
    "launch": {"interval_hours": 4, "label": "Launch"},
    "viral_referral": {"interval_hours": 4, "label": "Viral Referral"},
    "interactive": {"interval_hours": 4, "label": "Interactive"},
    "partnership": {"interval_hours": 3, "label": "Partnership"},
    "community": {"interval_hours": 2, "label": "Community"},
    "pricing": {"interval_hours": 6, "label": "Pricing"},
    "content": {"interval_hours": 2, "label": "Content"},
    "trend_jacker": {"interval_hours": 1, "label": "Trend Jacker"},
    "neuromarketing": {"interval_hours": 3, "label": "Neuromarketing"},
}

_running = False

AGENT_PROMPTS = {
    "market_research": "Analyze current market trends and opportunities for Gumroad digital products. Identify gaps and emerging niches.",
    "launch": "Create a multi-platform product launch strategy for Gumroad products (Product Hunt, Hacker News, Betalist, etc).",
    "viral_referral": "Design a viral referral campaign with tiered rewards, gamification, and affiliate mechanics.",
    "interactive": "Design an interactive content experience with ROI calculator, assessment quiz, and lead capture.",
    "partnership": "Identify and design partnership outreach strategy with complementary Gumroad creators and newsletter owners.",
    "community": "Design community engagement strategies, ambassador programs, and UGC campaigns.",
    "pricing": "Analyze pricing optimization opportunities based on market positioning and competitor analysis.",
    "content": "Design a content strategy including SEO-optimized articles, lead magnets, and content upgrades.",
    "trend_jacker": "Identify current trending topics and create a trend-jacking content strategy.",
    "neuromarketing": "Apply neuromarketing principles to optimize product pages, CTAs, and email sequences.",
}


async def run_scheduled_agent(agent_name: str, user: User):
    """Run a single scheduled agent with AI-generated content"""
    factory = get_session_factory()
    config = SCHEDULE_CONFIG.get(agent_name, {})

    # Log start
    async with factory() as db:
        try:
            activity = AgentActivity(
                user_id=user.id,
                agent_name=agent_name,
                action=f"تشغيل {config.get('label', agent_name)}",
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

    # Generate AI content (no DB session held during AI call)
    result = None
    error = None
    try:
        prompt = AGENT_PROMPTS.get(agent_name)
        if prompt:
            ai = MultiAIService()
            raw = await ai.chat(
                messages=[
                    {"role": "system", "content": "أنت خبير تسويق رقمي. استخدم العربية في الرد. قدم تحليلاً مفصلاً."},
                    {"role": "user", "content": f"{prompt}\n\nقدم استراتيجية قابلة للتنفيذ خطوة بخطوة."},
                ],
                temperature=0.7,
                max_tokens=2000,
            )
            result = {"content": raw, "agent": agent_name, "status": "completed"}
        elif agent_name in ("email_3d", "seo_empire"):
            engine = InnovationMarketingEngine(user_id=user.id)
            product = {"name": "Gumroad Product", "price": 29.99, "description": "Digital product"}
            result = await engine.execute_channel(agent_name, product)
        else:
            ai = MultiAIService()
            raw = await ai.chat(
                messages=[
                    {"role": "system", "content": "أنت خبير تسويق رقمي متخصص."},
                    {"role": "user", "content": f"اعمل تحليل واستراتيجية كـ {config.get('label', agent_name)}. قدم recommendations قابلة للتنفيذ."},
                ],
                temperature=0.7,
                max_tokens=1500,
            )
            result = {"content": raw, "agent": agent_name, "status": "completed"}
    except Exception as e:
        error = str(e)
        print(f"[Scheduler] Agent execution error for {agent_name}: {e}")

    # Log completion and update session
    async with factory() as db:
        try:
            result_entry = await db.execute(
                select(AgentActivity).where(
                    AgentActivity.user_id == user.id,
                    AgentActivity.agent_name == agent_name,
                    AgentActivity.status == "running",
                ).order_by(AgentActivity.id.desc()).limit(1)
            )
            act = result_entry.scalar_one_or_none()
            if act:
                act.status = "completed" if not error else "failed"
                act.output_data = str(result)[:1000] if result else None
                act.error_message = error
                act.duration_ms = 0
                await db.commit()

                await broadcast_activity({
                    "type": "activity",
                    "agent_name": agent_name,
                    "action": f"اكتمل {config.get('label', agent_name)}",
                    "status": "completed" if not error else "failed",
                    "preview": str(result)[:200] if result else error,
                    "activity_id": act.id,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })

            result_s = await db.execute(
                select(AgentSession).where(
                    AgentSession.user_id == user.id,
                    AgentSession.agent_name == agent_name,
                )
            )
            session = result_s.scalar_one_or_none()
            if session:
                session.total_runs = (session.total_runs or 0) + 1
            await db.commit()
        except Exception as e:
            print(f"[Scheduler] Log completion error: {e}")


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
    print(f"[Scheduler] Started with {len(SCHEDULE_CONFIG)} agents")
    return task


def stop_scheduler():
    """Stop the background scheduler"""
    global _running
    _running = False
    print("[Scheduler] Stopped background scheduler")
