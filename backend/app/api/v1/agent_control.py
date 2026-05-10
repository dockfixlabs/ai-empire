"""Agent Control Center - Full control & monitoring"""
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.core.database import get_db
from app.models.user import User
from app.models.activity import AgentActivity, AgentSession
from app.dependencies import get_current_user
from datetime import datetime, timezone
from typing import Optional
import asyncio
import json

router = APIRouter(prefix="/agents", tags=["Agent Control Center"])

ALL_AGENTS = [
    {"name": "market_research", "label": "أبحاث السوق", "icon": "🔍", "description": "تحليل الفرص والاتجاهات"},
    {"name": "email_3d", "label": "Email 3D", "icon": "📧", "description": "إيميلات سلوكية عميقة"},
    {"name": "seo_empire", "label": "SEO Empire", "icon": "🌐", "description": "إمبراطورية محتوى SEO"},
    {"name": "launch", "label": "Launch", "icon": "🚀", "description": "إطلاق متعدد المنصات"},
    {"name": "viral_referral", "label": "Viral Referral", "icon": "🔄", "description": "إحالة فيروسية"},
    {"name": "interactive", "label": "Interactive", "icon": "🎯", "description": "محتوى تفاعلي"},
    {"name": "partnership", "label": "Partnership", "icon": "🤝", "description": "شراكات تلقائية"},
    {"name": "community", "label": "Community", "icon": "👥", "description": "مجتمع نابض"},
    {"name": "pricing", "label": "Pricing", "icon": "💰", "description": "تحسين التسعير"},
    {"name": "content", "label": "Content", "icon": "✍️", "description": "استراتيجية المحتوى"},
    {"name": "trend_jacker", "label": "Trend Jacker", "icon": "📡", "description": "اصطياد الترندات"},
    {"name": "neuromarketing", "label": "Neuromarketing", "icon": "🧠", "description": "تسويق عصبي"},
]

# WebSocket connections
active_connections: list[WebSocket] = []


async def broadcast_activity(activity: dict):
    """Send activity update to all connected WebSocket clients"""
    dead = []
    for conn in active_connections:
        try:
            await conn.send_json(activity)
        except Exception:
            dead.append(conn)
    for conn in dead:
        active_connections.remove(conn)


@router.websocket("/ws")
async def agent_websocket(websocket: WebSocket):
    """WebSocket for live agent activity streaming"""
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep alive
    except WebSocketDisconnect:
        active_connections.remove(websocket)
    except Exception:
        if websocket in active_connections:
            active_connections.remove(websocket)


@router.get("/list")
async def list_agents_with_status(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all agents with their current status"""
    result = await db.execute(
        select(AgentSession).where(AgentSession.user_id == user.id)
    )
    sessions = {(s.agent_name, s) for s in result.scalars().all()}
    session_map = {s.agent_name: s for _, s in sessions}

    agents = []
    for agent in ALL_AGENTS:
        s = session_map.get(agent["name"])
        agents.append({
            **agent,
            "is_running": s.is_running if s else False,
            "total_runs": s.total_runs if s else 0,
            "total_errors": s.total_errors if s else 0,
            "last_started_at": s.last_started_at.isoformat() if s and s.last_started_at else None,
        })
    return {"agents": agents}


@router.get("/logs")
async def get_agent_logs(
    agent_name: Optional[str] = None,
    limit: int = 50,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get agent activity logs"""
    query = select(AgentActivity).where(AgentActivity.user_id == user.id)
    if agent_name:
        query = query.where(AgentActivity.agent_name == agent_name)
    query = query.order_by(desc(AgentActivity.created_at)).limit(limit)
    result = await db.execute(query)
    logs = []
    for act in result.scalars().all():
        logs.append({
            "id": act.id,
            "agent_name": act.agent_name,
            "action": act.action,
            "status": act.status,
            "input_data": act.input_data,
            "output_preview": (act.output_data or "")[:200],
            "error_message": act.error_message,
            "duration_ms": act.duration_ms,
            "created_at": act.created_at.isoformat() if act.created_at else None,
        })
    return {"logs": logs, "total": len(logs)}


@router.post("/{agent_name}/start")
async def start_agent(
    agent_name: str,
    data: Optional[dict] = {},
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Start/trigger an agent"""
    agent_names = {a["name"] for a in ALL_AGENTS}
    if agent_name not in agent_names:
        raise HTTPException(400, f"Unknown agent: {agent_name}")

    from app.core.database import get_session_factory
    factory = get_session_factory()

    # Use isolated session for all DB writes to avoid SQLite locking
    activity_id = None
    async with factory() as write_db:
        try:
            result = await write_db.execute(
                select(AgentSession).where(
                    AgentSession.user_id == user.id,
                    AgentSession.agent_name == agent_name,
                )
            )
            session = result.scalar_one_or_none()
            if not session:
                session = AgentSession(
                    user_id=user.id,
                    agent_name=agent_name,
                    is_running=True,
                    config=data.get("config"),
                )
                write_db.add(session)
            else:
                session.is_running = True
                session.last_started_at = datetime.now(timezone.utc)
                session.total_runs = (session.total_runs or 0) + 1

            activity = AgentActivity(
                user_id=user.id,
                agent_name=agent_name,
                action=f"Started {agent_name}",
                status="running",
                input_data=data,
            )
            write_db.add(activity)
            await write_db.flush()
            await write_db.commit()
            activity_id = activity.id
        except Exception as e:
            await write_db.rollback()
            raise HTTPException(500, f"Database error: {str(e)}")

    # Broadcast via WebSocket
    await broadcast_activity({
        "type": "agent_started",
        "agent_name": agent_name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "activity_id": activity_id,
    })

    return {"status": "started", "agent": agent_name, "activity_id": activity_id}


@router.post("/{agent_name}/stop")
async def stop_agent(
    agent_name: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Stop an agent"""
    result = await db.execute(
        select(AgentSession).where(
            AgentSession.user_id == user.id,
            AgentSession.agent_name == agent_name,
        )
    )
    session = result.scalar_one_or_none()
    if session:
        session.is_running = False
        session.last_stopped_at = datetime.now(timezone.utc)

    await db.flush()

    # Broadcast
    await broadcast_activity({
        "type": "agent_stopped",
        "agent_name": agent_name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })

    return {"status": "stopped", "agent": agent_name}


@router.post("/log")
async def log_activity(
    data: dict,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Log an agent activity (called by agents themselves)"""
    activity = AgentActivity(
        user_id=user.id,
        agent_name=data.get("agent_name", "unknown"),
        action=data.get("action", "unknown"),
        status=data.get("status", "completed"),
        input_data=data.get("input_data"),
        output_data=json.dumps(data.get("output_data", {}), ensure_ascii=False) if data.get("output_data") else None,
        error_message=data.get("error"),
        duration_ms=data.get("duration_ms"),
        completed_at=datetime.now(timezone.utc) if data.get("status") in ("completed", "failed") else None,
    )
    db.add(activity)
    await db.flush()

    # Broadcast
    await broadcast_activity({
        "type": "activity",
        "agent_name": activity.agent_name,
        "action": activity.action,
        "status": activity.status,
        "timestamp": activity.created_at.isoformat() if activity.created_at else None,
        "activity_id": activity.id,
        "preview": (activity.output_data or "")[:150],
    })

    return {"logged": True, "activity_id": activity.id}
