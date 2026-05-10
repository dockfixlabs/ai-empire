from typing import Optional, Dict, Any, List
from agents.base import AgentBase


class InfluencerMatcherAgent(AgentBase):
    INFLUENCER_TIERS = [
        {"tier": "nano", "followers": "1k-10k", "engagement": "5-10%", "cost": "free-product"},
        {"tier": "micro", "followers": "10k-100k", "engagement": "3-6%", "cost": "$50-500"},
        {"tier": "mid", "followers": "100k-500k", "engagement": "2-4%", "cost": "$500-2000"},
        {"tier": "macro", "followers": "500k-1M", "engagement": "1-3%", "cost": "$2000-5000"},
    ]

    async def run(self, campaign_id: str = None, **kwargs) -> Dict[str, Any]:
        result = await self.generate_json(
            system_prompt="""You are an influencer marketing strategist who finds perfect creator partnerships.
Output JSON with:
- influencer_profiles: list of ideal influencer types with: niche, follower_range, engagement_minimum, content_style, audience_demographics, brand_fit_score_min
- search_parameters: keywords, hashtags, platforms to search
- outreach_strategy: template, personalization_framework, follow_up_sequence
- partnership_tiers: different collaboration levels from free product to paid sponsorship
- content_briefs: what each influencer tier should create
- campaign_integration: how influencer content feeds into main campaign
- measurement_framework: engagement, referral traffic, conversions, promo_code_usage
- budget_estimate: cost projection by tier mix
- expected_roi: projected return per tier""",
            user_prompt=f"Find and match influencers for campaign {campaign_id}. Focus on micro and nano influencers with high engagement. Prioritize authentic fit over follower count."
        )

        result["influencers_found"] = len(result.get("influencer_profiles", []))
        result["tiers_available"] = [t["tier"] for t in self.INFLUENCER_TIERS]
        self.log_performance("influencer_matcher", result)
        return result
