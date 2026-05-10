from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
from agents.base import AgentBase


class SocialMediaAgent(AgentBase):
    PLATFORMS = {
        "twitter": {"chars": 280, "best_times": ["7-9am", "12-1pm", "5-6pm"], "format": "text"},
        "linkedin": {"chars": 3000, "best_times": ["7-9am", "12-1pm", "5-6pm"], "format": "professional"},
        "instagram": {"chars": 2200, "best_times": ["9-11am", "7-9pm"], "format": "visual"},
        "tiktok": {"chars": 150, "best_times": ["7-10am", "7-11pm"], "format": "video"},
        "youtube": {"chars": 5000, "best_times": ["2-4pm", "6-8pm"], "format": "video_long"},
    }

    async def run(self, campaign_id: str = None, **kwargs) -> Dict[str, Any]:
        result = {
            "campaign_id": campaign_id,
            "posts_created": 0,
            "platforms_activated": [],
            "content": {},
            "status": "completed",
        }

        for platform, config in self.PLATFORMS.items():
            post = await self._create_platform_post(platform, config, campaign_id or "default")
            if post:
                result["posts_created"] += 1
                result["platforms_activated"].append(platform)
                result["content"][platform] = post

        self.log_performance("social_media", result)
        return result

    async def _create_platform_post(self, platform: str, config: Dict, campaign_id: str) -> Optional[Dict]:
        post = await self.generate_json(
            system_prompt=f"""You are a {platform} content expert. You write native content that performs optimally on this platform.
Output JSON with: content, hook, hashtags (up to 5), best_time, visual_notes.""",
            user_prompt=f"""Create a high-performance {platform} post for campaign {campaign_id}.
Platform specs: max {config['chars']} chars, best times: {config['best_times']}.
Format: {config['format']}.

Apply platform-specific hooks and optimize for the algorithm."""
        )
        return post

    async def optimize_post_timing(self, platform: str, audience_timezone: str) -> List[str]:
        return self.PLATFORMS.get(platform, {}).get("best_times", ["12pm"])

    async def create_content_series(self, campaign_id: str, platform: str, count: int = 5) -> List[Dict]:
        series = []
        for i in range(count):
            post = await self._create_platform_post(
                platform, self.PLATFORMS.get(platform, {}), campaign_id
            )
            if post:
                post["day"] = i + 1
                series.append(post)
        return series
