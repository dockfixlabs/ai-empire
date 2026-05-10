from typing import Optional, Dict, Any, List
from agents.base import AgentBase


class ConversionOptimizer(AgentBase):
    CONVERSION_PRINCIPLES = [
        "clear_value_proposition", "social_proof", "urgency",
        "scarcity", "authority_signals", "trust_badges",
        "risk_reversal", "guarantees", "testimonials",
        "case_studies", "objection_handling", "fomo_triggers",
        "visual_hierarchy", "CTA_contrast", "mobile_optimization",
        "load_speed", "checkout_simplification", "exit_intent",
    ]

    async def run(self, campaign_id: str = None, **kwargs) -> Dict[str, Any]:
        result = await self.generate_json(
            system_prompt="""You are a conversion rate optimization (CRO) expert who turns browsers into buyers.
Output JSON with:
- conversion_funnel: stage-by-stage with drop-off points and improvement strategies
- landing_page_optimizations: specific changes to increase conversion
- cta_optimization: button text, color, placement, size, urgency
- trust_elements: what to add (badges, testimonials, guarantees, case studies)
- objection_handling: common objections and counter-arguments
- checkout_optimization: reduce friction, increase completion
- mobile_optimizations: specific mobile improvements
- social_proof_deployment: where and how to place social proof
- urgency_mechanics: ethical urgency throughout the funnel
- a_b_test_priorities: ranked hypotheses to test
- predicted_lift: expected conversion rate improvement per change""",
            user_prompt=f"Optimize conversion funnel for campaign {campaign_id}."
        )

        result["principles_applied"] = self.CONVERSION_PRINCIPLES
        self.log_performance("conversion_optimizer", result)
        return result
