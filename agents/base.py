from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
from app.core.config import get_settings
from app.services.multi_ai import MultiAIService

settings = get_settings()


class AgentBase(ABC):
    def __init__(self, user_id: str, api_key: Optional[str] = None):
        self.user_id = user_id
        self.ai = MultiAIService(api_key=api_key)
        self.name = self.__class__.__name__
        self.created_at = datetime.now(timezone.utc)
        self.memory: Dict[str, Any] = {}
        self.performance_log: List[Dict] = []

    @abstractmethod
    async def run(self, *args, **kwargs) -> Any:
        pass

    async def think(self, context: str, instruction: str) -> str:
        messages = [
            {"role": "system", "content": f"""You are {self.name}, a specialized AI agent.
Your thinking process should be deep, strategic, and creative.

Context: {context}

Instruction: {instruction}

Think step by step before responding. Consider edge cases, psychological factors,
market dynamics, and innovative approaches. Be bold but practical."""},
        ]
        return await self.ai.chat(messages, temperature=0.7)

    async def generate_json(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        return await self.ai.generate_json(system_prompt, user_prompt)

    def log_performance(self, action: str, result: Any, duration_ms: float = 0):
        self.performance_log.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "agent": self.name,
            "action": action,
            "duration_ms": duration_ms,
        })

    def get_stats(self) -> Dict[str, Any]:
        return {
            "agent": self.name,
            "total_actions": len(self.performance_log),
            "created_at": self.created_at.isoformat(),
            "memory_keys": list(self.memory.keys()),
        }
