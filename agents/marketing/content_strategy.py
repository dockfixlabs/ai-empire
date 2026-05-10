from typing import Optional, Dict, Any, List
from agents.base import AgentBase


class ContentStrategyAgent(AgentBase):
    CONTENT_FORMATS = [
        "twitter_thread", "linkedin_article", "instagram_carousel", "tiktok_video",
        "youtube_short", "email_sequence", "blog_post", "podcast_episode",
        "infographic", "case_study", "checklist", "template", "worksheet",
        "webinar", "live_stream", "newsletter", "ebook_chapter", "video_tutorial",
    ]

    CONTENT_PILLARS = [
        "educational", "inspirational", "entertaining", "aspirational",
        "controversial", "behind_scenes", "user_generated", "curated",
        "original_research", "comparison", "storytelling", "how_to",
        "industry_news", "personal_journey", "expert_interview",
    ]

    async def run(self, product_id: str = None, market_data: Dict = None,
                  psychographic: Dict = None, **kwargs) -> Dict[str, Any]:
        thinking = await self.think(
            f"Create content strategy for product_id={product_id}",
            "Design a comprehensive content strategy that generates demand across 18 formats and 15 content pillars. Use the Content Atomization approach: one core insight → dozens of content pieces across all platforms."
        )

        result = await self.generate_json(
            system_prompt="""You are a world-class content strategist who creates systems, not just calendars.
Output JSON with:
- core_narrative: the overarching story that ties all content together
- content_pillars: 3-5 pillars with: pillar_name, topics (5-10), formats_to_use, posting_cadence
- atomization_map: for each core insight, list all the content pieces across all platforms
- channel_strategy: per platform: content_type, frequency, best_times, optimization_tips
- content_calendar: 30-day detailed calendar with day, platform, format, hook, goal
- seo_content_plan: content designed specifically for search traffic
- viral_seeding: which content pieces to seed where
- engagement_loops: how content drives comments, shares, saves
- pillar_upgrades: how to repurpose best-performing content
- kpi_targets: engagement rate, reach, shares, saves per platform""",
            user_prompt=f"""Create a 30-day content strategy:

Product Info: {str(market_data.get('product_opportunity', {})) if market_data else 'digital product'}
Audience Profile: {str(psychographic.get('psychographic_profile', {})) if psychographic else 'target audience'}
Primary Channels: Twitter/X, LinkedIn, Instagram, TikTok, Email, Blog

Content formats available: {', '.join(self.CONTENT_FORMATS)}
Content pillars: {', '.join(self.CONTENT_PILLARS)}

Apply the Content Atomization Framework:
1. Create 1 core deep insight per week
2. Atomize into: 1 long-form + 3 medium + 10 micro pieces
3. Each platform gets native-format content (not reposts)
4. Cross-link content to create webs
5. Optimize each piece for the platform's algorithm

Also apply:
- Topic Clusters (pillar page + cluster content)
- Skyscraper Technique (make content 10x better than competitors)
- Content Pruning (what to stop doing)
- Repurposing Waterfall (one format → many)

Thinking: {thinking[:300]}"""
        )

        result["total_formats"] = len(self.CONTENT_FORMATS)
        result["total_pillars"] = len(self.CONTENT_PILLARS)
        self.log_performance("content_strategy", result)
        return result

    async def atomize_content(self, core_insight: str) -> Dict[str, List[str]]:
        return await self.generate_json(
            system_prompt="You atomize one insight into content pieces for every platform. Output JSON with platform as key and list of content ideas as value.",
            user_prompt=f"Atomize this insight into content for all platforms: '{core_insight}'"
        )
