from typing import Optional, Dict, Any, List
from agents.base import AgentBase


class ViralEngine(AgentBase):
    VIRAL_TRIGGERS = [
        "curiosity_gap", "social_identity", "emotional_contagion",
        "practical_value", "status_signaling", "moral_outrage",
        "awe_inspiration", "humor_relief", "fear_urgency",
        "community_belonging", "identity_reinforcement", "novelty_shock"
    ]

    VIRAL_FORMATS = [
        "thread_tweetstorm", "short_form_video", "infographic_carousel",
        "challenge_hashtag", "comparison_showdown", "behind_scenes",
        "transformation_story", "listicle_hack", "controversial_take",
        "data_revelation", "ultimate_guide", "case_study_breakdown",
    ]

    async def run(self, product_id: str = None, market_data: Dict = None,
                  psychographic: Dict = None, **kwargs) -> Dict[str, Any]:
        thinking = await self.think(
            f"Create viral strategy for product_id={product_id}",
            "Design a viral marketing engine. Apply 12 viral triggers, 12 formats, and 7 viral loop mechanisms. Consider: emotional payload, shareability mechanics, network effects, platform algorithms, and meme potential."
        )

        result = await self.generate_json(
            system_prompt="""You are the world's top viral marketing engineer. You design viral systems that create exponential growth.
Output JSON with:
- viral_score_prediction: float 0-100
- primary_triggers: list of emotional/psychological triggers
- viral_mechanisms: list of how sharing happens
- content_blueprints: list of 5 viral content pieces with: hook, format, platform, emotional_angle, predicted_reach
- loop_design: how the viral cycle works
- seeding_strategy: where and how to seed initial content
- platform_algorithm_hacks: how to exploit each platform's algorithm
- meme_engineering: template for creating shareable variations
- timeline: expected viral trajectory by day
- amplification_tactics: list of force-multiplier tactics""",
            user_prompt=f"""Design a viral engine for:
Product: {str(market_data.get('product_opportunity', {})) if market_data else 'digital product'}
Audience: {str(psychographic.get('profile', {})) if psychographic else 'target audience'}

Apply these viral loop mechanisms:
1. PRODUCT-LED VIRALITY: Product itself creates sharing
2. CONTENT-LED VIRALITY: Content is inherently shareable
3. NETWORK-LED VIRALITY: Leverages existing networks
4. INCENTIVE-LED VIRALITY: Rewards for sharing
5. EMOTION-LED VIRALITY: Emotional payload triggers sharing
6. IDENTITY-LED VIRALITY: Sharing signals identity
7. UTILITY-LED VIRALITY: Useful content spreads naturally

Viral factors to optimize:
- K-factor (shares per user × conversion per share)
- Cycle time (how fast sharing happens)
- Platform leverage (algorithmic amplification)
- Emotional payload (intensity of emotional response)
- Social currency (does sharing make the person look good?)

Thinking seed: {thinking[:300]}"""
        )

        result["k_factor_estimate"] = self._estimate_k_factor(result)
        result["viral_triggers_applied"] = self.VIRAL_TRIGGERS
        self.log_performance("viral_engine", result)
        return result

    def _estimate_k_factor(self, strategy: Dict) -> float:
        score = len(strategy.get("viral_mechanisms", [])) * 0.15
        score += len(strategy.get("content_blueprints", [])) * 0.08
        score += len(strategy.get("amplification_tactics", [])) * 0.1
        return min(round(score, 2), 5.0)

    async def generate_viral_content(self, product_id: str, platform: str) -> Dict[str, Any]:
        return await self.generate_json(
            system_prompt="You create viral-worthy content optimized for specific platforms. Output JSON with hook, content, visual_notes, timing.",
            user_prompt=f"Create viral content for product_id={product_id} on {platform}. Apply platform-specific hooks and formats."
        )

    async def score_virality(self, content_hook: str) -> Dict[str, float]:
        result = await self.generate_json(
            system_prompt="You predict virality scores for content hooks. Score each factor 0-100. Output JSON.",
            user_prompt=f"Score this hook for virality potential: '{content_hook}'. Assess: curiosity, emotional impact, shareability, timeliness, platform fit, audience resonance."
        )
        return result
