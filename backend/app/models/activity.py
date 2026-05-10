from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime, timezone


class AgentActivity(Base):
    __tablename__ = "agent_activities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    agent_name = Column(String(100), nullable=False, index=True)
    action = Column(String(200), nullable=False)
    status = Column(String(20), default="running")  # running, completed, failed
    input_data = Column(JSON, nullable=True)
    output_data = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    duration_ms = Column(Float, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", backref="agent_activities")


class AgentSession(Base):
    __tablename__ = "agent_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    agent_name = Column(String(100), nullable=False)
    is_running = Column(Boolean, default=False)
    last_started_at = Column(DateTime, nullable=True)
    last_stopped_at = Column(DateTime, nullable=True)
    total_runs = Column(Integer, default=0)
    total_errors = Column(Integer, default=0)
    config = Column(JSON, nullable=True)

    user = relationship("User", backref="agent_sessions")
