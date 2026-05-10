from typing import Optional, Dict, Any, List
from agents.base import AgentBase
from datetime import datetime, timedelta


class EmailAutomationAgent(AgentBase):
    SEQUENCE_TYPES = {
        "welcome": {"emails": 3, "days": [0, 1, 3]},
        "launch": {"emails": 7, "days": [0, 1, 2, 4, 7, 10, 14]},
        "abandoned_cart": {"emails": 3, "days": [0, 1, 3]},
        "re_engagement": {"emails": 2, "days": [0, 7]},
        "post_purchase": {"emails": 4, "days": [0, 2, 7, 14]},
        "nurture": {"emails": 5, "days": [0, 2, 5, 10, 20]},
    }

    async def run(self, campaign_id: str = None, **kwargs) -> Dict[str, Any]:
        result = {
            "campaign_id": campaign_id,
            "sequences_created": [],
            "total_emails": 0,
            "status": "completed",
        }

        sequences = [
            ("welcome", "New subscribers"),
            ("nurture", "Warm leads"),
            ("launch", "Launch sequence"),
            ("post_purchase", "Existing customers"),
        ]

        for seq_type, audience in sequences:
            seq = await self._create_sequence(seq_type, audience, campaign_id or "default")
            result["sequences_created"].append({
                "type": seq_type,
                "audience": audience,
                "emails": seq,
                "email_count": len(seq),
            })
            result["total_emails"] += len(seq)

        self.log_performance("email_automation", result)
        return result

    async def _create_sequence(self, seq_type: str, audience: str, campaign_id: str) -> List[Dict]:
        config = self.SEQUENCE_TYPES.get(seq_type, {"emails": 3, "days": [0, 1, 3]})
        emails = []

        for i in range(config["emails"]):
            day = config["days"][i] if i < len(config["days"]) else config["days"][-1] + (i * 2)
            email = await self.generate_json(
                system_prompt="""You are a world-class email marketer. You write emails that get opened, clicked, and converted.
Output JSON with: subject_line, preview_text, body_html_structure, cta, psychological_triggers_used, predicted_open_rate, predicted_click_rate.""",
                user_prompt=f"""Write email {i+1} of {config['emails']} for {seq_type} sequence.
Audience: {audience}
Day: {day} (from sequence start)
Campaign: {campaign_id}

Apply these email marketing principles:
- Curiosity gap in subject lines
- Personalization beyond just name
- Value-first, ask-second structure
- Scarcity and urgency in launch emails
- Social proof integration
- Clear singular CTA per email
- Mobile-optimized short paragraphs
- Story-driven narrative throughout sequence"""
            )
            email["sequence_position"] = i + 1
            email["send_day"] = day
            emails.append(email)

        return emails

    async def write_launch_sequence(self, product_name: str, launch_date: datetime) -> List[Dict]:
        campaign_id = f"launch_{product_name.lower().replace(' ', '_')}"
        return await self._create_sequence("launch", "Launch audience", campaign_id)
