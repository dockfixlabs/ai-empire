from typing import Optional, Dict, Any, List
from agents.base import AgentBase


class CommunityBuilder(AgentBase):
    COMMUNITY_PLATFORMS = [
        "discord", "facebook_group", "slack_community",
        "subreddit", "circle_so", "skool",
    ]

    async def run(self, campaign_id: str = None, **kwargs) -> Dict[str, Any]:
        result = await self.generate_json(
            system_prompt="""You are a community-building expert who creates thriving, engaged communities around products.
Output JSON with:
- community_blueprint: platform_choice, structure, channels/categories, size_targets
- engagement_mechanics: daily/weekly activities, rituals, traditions, challenges
- growth_strategy: how to attract first 100, 1000, 10000 members
- moderation_plan: rules, roles, escalation paths, automod
- value_creation: what value does the community provide beyond the product
- member_journey: from newbie to elder — progression path
- gamification: badges, levels, leaderboards, special access
- user_generated_content: how to inspire members to create
- events_calendar: AMAs, workshops, challenges, meetups
- monetization: how community drives product sales
- metrics: engagement rate, retention, referral rate, NPS""",
            user_prompt=f"""Design a community strategy for campaign {campaign_id}.

Community-first principles:
1. Community before product (build audience first)
2. Members as co-creators (involve them in product development)
3. UGC engine (members creating content for each other)
4. Peer-to-peer value (members helping members)
5. Exclusive access (community-only perks)
6. Identity badge (being a member signals something)

Available platforms: {', '.join(self.COMMUNITY_PLATFORMS)}"""
        )

        result["community_platforms"] = self.COMMUNITY_PLATFORMS
        self.log_performance("community_builder", result)
        return result
