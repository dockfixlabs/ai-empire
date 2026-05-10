from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
from agents.base import AgentBase
from agents.marketing.market_research import MarketResearchAgent
from agents.marketing.viral_engine import ViralEngine
from agents.marketing.content_strategy import ContentStrategyAgent
from agents.marketing.social_media import SocialMediaAgent
from agents.marketing.email_automation import EmailAutomationAgent
from agents.marketing.seo_engine import SEOEngine
from agents.marketing.trend_jacker import TrendJacker
from agents.marketing.community_builder import CommunityBuilder
from agents.marketing.influencer_matcher import InfluencerMatcherAgent
from agents.marketing.neuromarketing import NeuromarketingEngine
from agents.marketing.referral_engine import ReferralEngine
from agents.marketing.launch_controller import LaunchController
from agents.content.product_generator import ProductGeneratorAgent
from agents.sales.pricing_optimizer import PricingOptimizer
from agents.sales.conversion_optimizer import ConversionOptimizer


class AgentOrchestrator(AgentBase):
    def __init__(self, user_id: str, api_key: Optional[str] = None):
        super().__init__(user_id, api_key)
        self.agents: Dict[str, AgentBase] = {}
        self._init_agents()

    def _init_agents(self):
        self.agents = {
            "market_research": MarketResearchAgent(self.user_id),
            "viral_engine": ViralEngine(self.user_id),
            "content_strategy": ContentStrategyAgent(self.user_id),
            "social_media": SocialMediaAgent(self.user_id),
            "email_automation": EmailAutomationAgent(self.user_id),
            "seo_engine": SEOEngine(self.user_id),
            "trend_jacker": TrendJacker(self.user_id),
            "community_builder": CommunityBuilder(self.user_id),
            "influencer_matcher": InfluencerMatcherAgent(self.user_id),
            "neuromarketing": NeuromarketingEngine(self.user_id),
            "referral_engine": ReferralEngine(self.user_id),
            "launch_controller": LaunchController(self.user_id),
            "product_generator": ProductGeneratorAgent(self.user_id),
            "pricing_optimizer": PricingOptimizer(self.user_id),
            "conversion_optimizer": ConversionOptimizer(self.user_id),
        }

    async def run(self, task_type: str, **kwargs):
        agent = self.agents.get(task_type)
        if not agent:
            raise ValueError(f"Unknown agent type: {task_type}")
        return await agent.run(**kwargs)

    async def create_go_to_market_strategy(self, product_id: str) -> Dict[str, Any]:
        strategy = {
            "product_id": product_id,
            "phases": [],
            "agents_involved": [],
            "timeline": {},
        }

        market = await self.agents["market_research"].run(product_id=product_id)
        strategy["market_analysis"] = market
        strategy["agents_involved"].append("market_research")

        neuromarketing_profile = await self.agents["neuromarketing"].run(product_id=product_id, market_data=market)
        strategy["psychographic_profile"] = neuromarketing_profile
        strategy["agents_involved"].append("neuromarketing")

        pricing = await self.agents["pricing_optimizer"].run(product_id=product_id, market_data=market)
        strategy["pricing_strategy"] = pricing
        strategy["agents_involved"].append("pricing_optimizer")

        content_plan = await self.agents["content_strategy"].run(
            product_id=product_id,
            market_data=market,
            psychographic=neuromarketing_profile,
        )
        strategy["content_plan"] = content_plan
        strategy["agents_involved"].append("content_strategy")

        viral_strategy = await self.agents["viral_engine"].run(
            product_id=product_id,
            market_data=market,
            psychographic=neuromarketing_profile,
        )
        strategy["viral_strategy"] = viral_strategy
        strategy["agents_involved"].append("viral_engine")

        launch_plan = await self.agents["launch_controller"].run(
            product_id=product_id,
            content_plan=content_plan,
            viral_strategy=viral_strategy,
        )
        strategy["launch_plan"] = launch_plan
        strategy["agents_involved"].append("launch_controller")

        strategy["phases"] = launch_plan.get("phases", [])
        strategy["timeline"] = launch_plan.get("timeline", {})

        self.log_performance("create_go_to_market_strategy", strategy)
        return strategy

    async def execute_campaign(self, campaign_id: str) -> Dict[str, Any]:
        results = {
            "campaign_id": campaign_id,
            "channels_activated": [],
            "errors": [],
            "status": "in_progress",
        }

        social_result = await self.agents["social_media"].run(campaign_id=campaign_id)
        if social_result.get("status") == "error":
            results["errors"].append({"agent": "social_media", "error": social_result.get("error")})
        results["channels_activated"].append("social_media")

        email_result = await self.agents["email_automation"].run(campaign_id=campaign_id)
        results["channels_activated"].append("email")

        seo_result = await self.agents["seo_engine"].run(campaign_id=campaign_id)
        results["channels_activated"].append("seo")

        trend_result = await self.agents["trend_jacker"].run(campaign_id=campaign_id)
        if trend_result.get("opportunities_found", 0) > 0:
            results["channels_activated"].append("trend_jacking")
            results["trend_opportunities"] = trend_result.get("opportunities", [])

        community_result = await self.agents["community_builder"].run(campaign_id=campaign_id)
        results["channels_activated"].append("community")

        influencer_result = await self.agents["influencer_matcher"].run(campaign_id=campaign_id)
        if influencer_result.get("influencers_found", 0) > 0:
            results["channels_activated"].append("influencer_outreach")
            results["influencers"] = influencer_result.get("influencers", [])

        referral_plan = await self.agents["referral_engine"].run(campaign_id=campaign_id)
        results["referral_plan"] = referral_plan
        results["channels_activated"].append("referral")

        conversion_plan = await self.agents["conversion_optimizer"].run(campaign_id=campaign_id)
        results["conversion_optimizations"] = conversion_plan

        results["status"] = "active"
        results["total_channels"] = len(results["channels_activated"])
        results["total_errors"] = len(results["errors"])

        self.log_performance("execute_campaign", results)
        return results

    async def process_task(self, task_id: str, agent_type: str, task: str, context: Optional[Dict] = None):
        agent = self.agents.get(agent_type)
        if not agent:
            return {"task_id": task_id, "status": "error", "error": f"Unknown agent: {agent_type}"}

        result = await agent.run(task=task, context=context)
        return {"task_id": task_id, "status": "completed", "result": result}

    async def run(self, **kwargs):
        return await self.create_go_to_market_strategy(kwargs.get("product_id", ""))
