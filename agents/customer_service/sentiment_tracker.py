from typing import Optional, Dict, Any, List
from agents.base import AgentBase


class SentimentTracker(AgentBase):
    async def run(self, messages: List[str] = None, **kwargs) -> Dict[str, Any]:
        result = await self.generate_json(
            system_prompt="""You are a customer sentiment analysis expert.
Output JSON with:
- overall_sentiment: positive/negative/neutral/mixed
- sentiment_score: float -1.0 to 1.0
- emotion_breakdown: dict with anger, joy, frustration, satisfaction, confusion, excitement scores
- trends: sentiment trend over time (improving, declining, stable)
- common_themes: recurring topics in feedback
- pain_points: specific issues mentioned
- praise_points: what customers love
- action_items: recommended responses to feedback
- priority_issues: what needs immediate attention""",
            user_prompt=f"Analyze sentiment from these customer messages: {messages or ['No messages provided']}"
        )

        self.log_performance("sentiment_tracker", result)
        return result
