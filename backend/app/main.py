import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select, func
from app.core.config import get_settings
from app.core.database import init_db, close_db, get_session_factory
from app.api.v1 import auth, products, marketing, agents, gumroad_integration, marketing_innovation, agent_control
from app.services.scheduler import start_scheduler, stop_scheduler
from app.models.activity import AgentActivity

settings = get_settings()
_scheduler_task = None
_startup_time = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _scheduler_task, _startup_time
    _startup_time = datetime.now(timezone.utc)
    await init_db()
    _scheduler_task = start_scheduler()
    yield
    stop_scheduler()
    await close_db()


app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = Path(__file__).parent.parent / "static"
if STATIC_DIR.exists():
    app.mount("/assets", StaticFiles(directory=str(STATIC_DIR / "assets")), name="assets")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"},
    )


app.include_router(auth.router, prefix="/api/v1")
app.include_router(products.router, prefix="/api/v1")
app.include_router(marketing.router, prefix="/api/v1")
app.include_router(agents.router, prefix="/api/v1")
app.include_router(gumroad_integration.router, prefix="/api/v1")
app.include_router(marketing_innovation.router, prefix="/api/v1")
app.include_router(agent_control.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "name": settings.app_name,
        "version": settings.version,
        "status": "operational",
        "agents": [a["name"] for a in agent_control.ALL_AGENTS],
    }


@app.get("/health")
async def health():
    return {"status": "healthy", "version": settings.version}


@app.get("/api/v1/system/status")
async def system_status():
    """Comprehensive system status endpoint"""
    uptime = None
    if _startup_time:
        delta = datetime.now(timezone.utc) - _startup_time
        uptime = int(delta.total_seconds())

    ai_status = "ok"
    ai_provider = settings.ai_provider or "auto"
    try:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.groq.com/openai/v1/models",
                headers={"Authorization": f"Bearer {settings.groq_api_key}"},
                timeout=aiohttp.ClientTimeout(total=5),
            ) as resp:
                if resp.status != 200:
                    ai_status = "error"
    except Exception:
        ai_status = "error"

    db_status = "ok"
    try:
        factory = get_session_factory()
        async with factory() as db:
            await db.execute(select(1))
    except Exception:
        db_status = "error"

    total_activities = 0
    try:
        factory = get_session_factory()
        async with factory() as db:
            result = await db.execute(select(func.count(AgentActivity.id)))
            total_activities = result.scalar() or 0
    except Exception:
        pass

    return {
        "system": {
            "name": settings.app_name,
            "version": settings.version,
            "status": "operational" if ai_status == "ok" and db_status == "ok" else "degraded",
            "uptime_seconds": uptime,
            "started_at": _startup_time.isoformat() if _startup_time else None,
            "platform": sys.platform,
            "python_version": sys.version.split()[0],
        },
        "database": {"status": db_status, "type": "sqlite" if "sqlite" in settings.database_url else "postgresql"},
        "ai": {"status": ai_status, "provider": ai_provider, "model": settings.groq_model},
        "websocket_connections": len(agent_control.active_connections),
        "total_activities": total_activities,
        "scheduler_active": _scheduler_task is not None and not _scheduler_task.done(),
    }


if STATIC_DIR.exists():

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        index = STATIC_DIR / "index.html"
        if index.exists():
            return FileResponse(str(index))
        return JSONResponse({"detail": "Not found"}, status_code=404)
