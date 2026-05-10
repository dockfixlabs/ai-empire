from typing import Optional, Dict, Any, List
from agents.base import AgentBase


class MarketResearchAgent(AgentBase):
    async def research(self, *args, **kwargs):
        return await self.run(**kwargs)
    async def run(self, product_id: str = None, niche: str = None,
                  keywords: List[str] = None, target_audience: str = None,
                  content_type: str = None, **kwargs) -> Dict[str, Any]:
        thinking = await self.think(
            f"Research opportunity in niche={niche}, keywords={keywords}, audience={target_audience}",
            "Conduct deep market research. Identify underserved needs, high-demand low-competition niches, and optimal product opportunities. Consider: trend trajectories, audience pain points, purchase intent signals, content gaps, and competitive weaknesses."
        )

        result = await self.generate_json(
            system_prompt="""You are a world-class market research AI. You analyze markets at an expert level.
Output MUST be valid JSON with these exact keys:
- niche_analysis: dict with description, size, growth_trend, seasonality
- competition: dict with level, top_competitors (list), gaps_found (list), barriers
- target_audience: dict with demographics, psychographics, pain_points (list), desires (list), objections (list)
- product_opportunity: dict with idea, description, suggested_format, unique_angle
- pricing: dict with suggested_price, price_range, anchoring_strategy
- demand_signals: list of evidence of demand
- keywords: list of high-intent keywords
- viral_angles: list of angles with viral potential
- confidence_score: float between 0 and 1
- recommendations: list of actionable next steps""",
            user_prompt=f"""Research this opportunity deeply:
Niche: {niche or 'digital products'}
Keywords: {keywords or ['online business', 'digital downloads', 'passive income']}
Target Audience: {target_audience or 'entrepreneurs and creators'}
Content Type: {content_type or 'digital product'}

Apply these advanced frameworks:
1. Blue Ocean Strategy - Find uncontested market space
2. Jobs To Be Done - What job is the customer hiring the product to do?
3. 5 Whys Analysis - Root cause of audience pain
4. Porter's Five Forces - Competitive landscape analysis
5. AIDA Model - Attention, Interest, Desire, Action gaps
6. Hook Model - What creates the habit loop?

Market Analysis: {thinking}"""
        )

        result["methodology"] = "multi_framework_analysis"
        result["thinking_seed"] = thinking[:200]
        self.log_performance("market_research", result)
        return result

    async def analyze_trends(self, niche: str) -> Dict[str, Any]:
        return await self.generate_json(
            system_prompt="You analyze market trends and predict trajectories. Output JSON.",
            user_prompt=f"Analyze current and future trends for '{niche}'. Predict 3-6 month trajectory."
        )

    async def find_content_gaps(self, niche: str) -> List[str]:
        result = await self.generate_json(
            system_prompt="You find content gaps and underserved topics in markets. Output JSON with gaps_found as array.",
            user_prompt=f"Find content gaps in '{niche}' niche. What are customers searching for but not finding?"
        )
        return result.get("gaps_found", [])
