from typing import Optional, Dict, Any, List
from agents.base import AgentBase


class SupportBotAgent(AgentBase):
    SUPPORT_CATEGORIES = [
        "product_question", "technical_issue", "pricing_inquiry",
        "download_problem", "refund_request", "account_issue",
        "license_key", "feature_request", "general_inquiry",
    ]

    async def run(self, customer_message: str = None, **kwargs) -> Dict[str, Any]:
        response = await self.generate_json(
            system_prompt="""You are an elite customer support AI that handles 95%+ of inquiries without human intervention.
Output JSON with:
- category: classified issue category
- sentiment: positive/neutral/negative/frustrated
- urgency: low/medium/high/critical
- response: empathetic, helpful, solution-oriented reply
- action_taken: what was done (answered, escalated, refunded, etc.)
- needs_human: bool (true if requires human agent)
- related_articles: list of FAQ/knowledge base articles to link
- follow_up_needed: bool and when
- satisfaction_prediction: predicted customer satisfaction (1-5)""",
            user_prompt=f"""Handle this customer inquiry:
Message: {customer_message or kwargs.get('message', 'How do I download my purchase?')}

Support categories: {', '.join(self.SUPPORT_CATEGORIES)}

Response principles:
1. Acknowledge emotion first ("I understand this is frustrating...")
2. Solve the problem, don't just answer the question
3. Be human (warm, conversational, not robotic)
4. Offer more than asked (anticipate next question)
5. Make it easy (step-by-step when needed)
6. Follow up (check if resolved)"""
        )

        response["handled"] = not response.get("needs_human", True)
        return response

    async def create_faq(self, product_data: Dict) -> List[Dict]:
        result = await self.generate_json(
            system_prompt="Generate comprehensive FAQ from product data. Output JSON with faqs array.",
            user_prompt=f"Generate 15-20 frequently asked questions for product: {product_data.get('title', 'digital product')}"
        )
        return result.get("faqs", [])
