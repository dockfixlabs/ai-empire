from typing import Optional, Dict, Any, List
from datetime import datetime, timezone, timedelta
from agents.base import AgentBase


class LaunchController(AgentBase):
    LAUNCH_WAVES = [
        "whisper", "tease", "preview", "early_access",
        "public_launch", "amplify", "sustain", "re_engage"
    ]

    async def run(self, product_id: str = None, content_plan: Dict = None,
                  viral_strategy: Dict = None, **kwargs) -> Dict[str, Any]:
        thinking = await self.think(
            f"Create multi-wave launch plan for product_id={product_id}",
            "Design a sophisticated 8-wave product launch strategy. Each wave has specific goals, channels, content types, and success metrics. Consider: sequential disclosure, scarcity building, social proof layering, and momentum compounding."
        )

        result = await self.generate_json(
            system_prompt="""You are a master launch strategist who creates Apple-level product launches for digital products.
Output JSON with:
- launch_strategy: overall framework name and philosophy
- waves: list of 7-8 waves, each with:
  - wave_name, duration_days, goals (list), channels (list)
  - content_plan (list of specific content pieces)
  - scarcity_mechanics (list of urgency tactics)
  - social_proof_targets (what proof to generate)
  - kpis (specific measurable metrics)
  - success_criteria (what determines wave completion)
- timeline: dict with pre_launch (X days), launch_day, post_launch (X days)
- scarcity_calendar: progressive scarcity across waves
- community_activation: how to mobilize community at each wave
- influencer_integration: when and how influencers participate
- contingency_plans: what if metrics underperform
- budget_allocations: spend per wave
- predicted_trajectory: expected sales curve""",
            user_prompt=f"""Design an 8-wave product launch:

Wave 1 - WHISPER (Days -30 to -21): Generate curiosity, no product reveal
Wave 2 - TEASE (Days -20 to -14): Hint at problem solution
Wave 3 - PREVIEW (Days -13 to -7): Show glimpses, build anticipation
Wave 4 - EARLY ACCESS (Days -6 to -3): Exclusive access to waitlist
Wave 5 - PUBLIC LAUNCH (Day 0): Full launch blitz
Wave 6 - AMPLIFY (Days +1 to +3): Social proof bombardment
Wave 7 - SUSTAIN (Days +4 to +14): Maintain momentum
Wave 8 - RE-ENGAGE (Days +15 to +30): Second wind, new angles

Content Plan: {str(content_plan.get('content_plan', {})) if content_plan else 'standard'}
Viral Strategy: {str(viral_strategy.get('viral_mechanisms', {})) if viral_strategy else 'standard'}

Apply these launch principles:
- Scarcity progression (less → more urgent)
- Social proof layering (testimonials → media mentions → sales numbers)
- Community FOMO (community members get early access)
- Sequential disclosure (reveal features over time)
- Anchoring (high anchor → real price feels like a deal)
- Reciprocity (free value before asking for sale)

Thinking: {thinking[:300]}"""
        )

        result["waves_count"] = len(result.get("waves", []))
        result["launch_duration_days"] = sum(
            w.get("duration_days", 1) for w in result.get("waves", [])
        )
        self.log_performance("launch_controller", result)
        return result

    async def calculate_launch_readiness(self, product_data: Dict) -> Dict[str, Any]:
        return await self.generate_json(
            system_prompt="You evaluate product launch readiness. Score categories 0-100. Output JSON with readiness_score and improvement_areas.",
            user_prompt=f"Score launch readiness for: {product_data}"
        )
