from typing import Optional, Dict, Any, List
from agents.base import AgentBase


class SEOEngine(AgentBase):
    async def run(self, campaign_id: str = None, **kwargs) -> Dict[str, Any]:
        result = await self.generate_json(
            system_prompt="""You are an elite SEO strategist who dominates search rankings.
Output JSON with:
- keyword_opportunities: list of high-value keywords with search_volume, competition, difficulty (0-100), intent, opportunity_score
- content_optimizations: list of specific on-page SEO improvements for the product page
- backlink_strategy: tiered plan for building backlinks
- technical_seo: checklist of technical improvements
- local_seo: if applicable
- featured_snippet_targets: questions to target for position zero
- pillar_cluster_strategy: topic cluster organization
- serp_analysis: current top 10 results for target keywords
- quick_wins: list of immediate actions with impact estimate""",
            user_prompt=f"""Create an SEO strategy for campaign {campaign_id}.

Focus on:
1. Keyword Research: Find long-tail keywords with high purchase intent
2. On-Page SEO: Title, H1-H6, meta description, URL structure, image alt text, schema markup
3. Content SEO: Topic clusters, internal linking, content depth
4. Technical SEO: Speed, mobile, Core Web Vitals, structured data
5. Off-Page SEO: Backlink acquisition strategy, guest posting, HARO
6. E-E-A-T: Experience, Expertise, Authoritativeness, Trustworthiness signals

Target: digital product search queries with buyer intent"""
        )

        self.log_performance("seo_engine", result)
        return result
