from typing import Optional, Dict, Any, List
from agents.base import AgentBase


class ReferralEngine(AgentBase):
    REFERRAL_MECHANICS = [
        "two_sided_reward", "points_system", "tiered_rewards",
        "contests_leaderboards", "exclusive_access", "cash_rebates",
        "discount_codes", "free_product", "charity_donation",
        "recognition_badges", "early_access", "community_status",
    ]

    GAMIFICATION_ELEMENTS = [
        "progress_bars", "levels", "achievements",
        "streaks", "challenges", "leaderboards",
        "unlockable_content", "virtual_currency", "prestige_system",
    ]

    async def run(self, campaign_id: str = None, **kwargs) -> Dict[str, Any]:
        result = await self.generate_json(
            system_prompt="""You design referral programs that turn customers into growth engines.
Output JSON with:
- referral_program_design: mechanics, rewards, terms, structures
- reward_architecture: what the referrer gets, what the referee gets
- viral_loop_design: step-by-step referral flow
- gamification_layer: badges, levels, leaderboards, challenges
- sharing_mechanisms: one-click share to each platform
- tracking_framework: attribution, cookie window, fraud detection
- optimization_plan: A/B test variables, iteration strategy
- predicted_metrics: referral rate, conversion rate, virality coefficient
- launch_plan: how to introduce the referral program
- segmentation: different programs for different customer tiers""",
            user_prompt=f"""Design a high-performance referral engine for campaign {campaign_id}.

Apply these referral mechanics: {', '.join(self.REFERRAL_MECHANICS)}
Gamification available: {', '.join(self.GAMIFICATION_ELEMENTS)}

Key principles:
1. Make sharing effortless (one-click, pre-written messages)
2. Make rewards irresistible (the referrer feels like they're winning)
3. Make the referee feel special (not just a discount, but an invitation)
4. Create status (top referrers get recognition)
5. Build in virality (each referral should lead to more referrals)
6. Measure everything (attribution, conversion, LTV by source)"""
        )

        self.log_performance("referral_engine", result)
        return result
