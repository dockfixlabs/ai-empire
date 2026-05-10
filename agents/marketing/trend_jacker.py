from typing import Optional, Dict, Any, List
from agents.base import AgentBase


class TrendJacker(AgentBase):
    TREND_SOURCES = [
        "twitter_trending", "reddit_hot", "google_trends",
        "news_headlines", "viral_topics", "industry_events",
        "cultural_moments", "seasonal_events", "celebrity_news",
        "product_launches", "policy_changes", "tech_announcements",
    ]

    async def run(self, campaign_id: str = None, **kwargs) -> Dict[str, Any]:
        result = await self.generate_json(
            system_prompt="""You are a real-time trend jacking specialist. You find trending topics and instantly create connections to your product.
Output JSON with:
- current_trends: list of detected trends with: trend_name, source, momentum (0-100), relevance_score, predicted_longevity_hours
- opportunities: list of trend jacking opportunities with: trend, angle_to_product, content_idea, platform, urgency, expected_engagement_lift
- risk_assessment: which trends to avoid (controversial, brand-damaging, etc.)
- action_plan: prioritized list of immediate actions with time windows
- monitoring_setup: what to watch for ongoing""",
            user_prompt=f"""Find and analyze trend jacking opportunities for campaign {campaign_id}.

Sources to monitor: {', '.join(self.TREND_SOURCES)}

For each opportunity, identify:
1. The trend (what's happening)
2. The connection (how it relates to our product)
3. The angle (our unique take)
4. The format (best content format for this trend)
5. The timing (when to strike — hours matter!)
6. The platform (where this trend lives)

Trend jacking principles:
- Speed is everything (first movers win big)
- Relevance matters (forced connections backfire)
- Add value (don't just exploit)
- Be authentic (audiences detect opportunism)
- Have a clear CTA (what should they do?)"""
        )

        result["opportunities_found"] = len(result.get("opportunities", []))
        result["sources_monitored"] = self.TREND_SOURCES
        self.log_performance("trend_jacker", result)
        return result
