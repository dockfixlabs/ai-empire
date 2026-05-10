from typing import Optional, Dict, Any, List
from agents.base import AgentBase


class NeuromarketingEngine(AgentBase):
    COGNITIVE_BIASES = [
        "anchoring", "social_proof", "scarcity", "authority",
        "liking", "reciprocity", "commitment_consistency",
        "loss_aversion", "framing_effect", "dunning_kruger",
        "bandwagon_effect", "decoy_effect", "endowment_effect",
        "halo_effect", "mere_exposure", "paradox_of_choice",
        "peak_end_rule", "serial_position", "chunking",
        "color_psychology", "price_relativity", "fear_of_missing_out"
    ]

    PERSUASION_FRAMEWORKS = [
        "Cialdini_7_Principles", "Minto_Pyramid", "StoryBrand_7_Parts",
        "AIDA_Model", "PAS_Framework", "FAB_Model",
        "BBP_Framework", "4Ps_Marketing", "Value_Proposition_Canvas"
    ]

    async def run(self, product_id: str = None, market_data: Dict = None,
                  **kwargs) -> Dict[str, Any]:
        thinking = await self.think(
            f"Create neuromarketing profile for product_id={product_id}",
            "Design a complete neuromarketing strategy. Apply 22 cognitive biases, 9 persuasion frameworks, and create a psychological profile of the target customer. Focus on: decision-making heuristics, emotional triggers, subconscious drivers, and persuasion architecture."
        )

        result = await self.generate_json(
            system_prompt="""You are a world-class neuromarketer and consumer psychologist. You understand the subconscious drivers of buying decisions at a deep level.
Output JSON with:
- psychographic_profile: dict with values, fears, aspirations, identity markers, decision_factors, information_processing_style
- bias_stack: list of 3-5 biases to apply in sequence with: bias_name, application_context, expected_effect, ethical_consideration
- persuasion_architecture: step-by-step buyer journey from attention to purchase using chosen frameworks
- messaging_framework: key messages mapped to psychological triggers
- color_psychology: recommended color palette linked to emotional response
- pricing_psychology: anchoring strategy, decoy options, charm pricing
- urgency_triggers: ethical scarcity and urgency mechanisms
- social_proof_blueprint: how to build and display social proof
- trust_architecture: credibility building elements
- objection_overrides: psychological reframes for common objections
- peak_end_design: how to create memorable positive experiences""",
            user_prompt=f"""Build a complete neuromarketing strategy for:
Product Data: {str(market_data.get('product_opportunity', {})) if market_data else 'digital product'}
Target Audience: {str(market_data.get('target_audience', {})) if market_data else 'entrepreneurs'}

Apply these in sequence for maximum persuasion:
1. FIRST IMPRESSION: Halo effect, mere exposure, color psychology
2. ATTENTION GRAB: Curiosity gap, novelty, contrast principle
3. INTEREST BUILD: StoryBrand framework, social proof, authority
4. DESIRE CREATE: Loss aversion, endowment effect, social identity
5. OBJECTION HANDLE: Framing effect, paradox of choice management
6. ACTION URGE: Scarcity, FOMO, commitment consistency
7. POST-PURCHASE: Peak-end rule, cognitive dissonance reduction

Cognitive biases available: {', '.join(self.COGNITIVE_BIASES)}
Frameworks available: {', '.join(self.PERSUASION_FRAMEWORKS)}

Thinking: {thinking[:300]}"""
        )

        result["biases_used"] = self.COGNITIVE_BIASES
        result["frameworks_used"] = self.PERSUASION_FRAMEWORKS
        result["psychological_depth"] = "advanced"
        self.log_performance("neuromarketing", result)
        return result

    async def analyze_conversion_psychology(self, landing_page_content: str) -> Dict[str, Any]:
        return await self.generate_json(
            system_prompt="You analyze content through a neuromarketing lens. Output JSON with psychology_score, friction_points, persuasion_opportunities.",
            user_prompt=f"Apply neuromarketing analysis to this content: {landing_page_content[:2000]}"
        )
