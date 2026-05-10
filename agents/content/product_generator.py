from typing import Optional, Dict, Any, List
from agents.base import AgentBase


class ProductGeneratorAgent(AgentBase):
    async def run(self, product_id: str = None, **kwargs) -> Dict[str, Any]:
        result = await self.generate_json(
            system_prompt="""You are a world-class digital product creator. You create high-value, sellable digital products.
Output JSON with:
- product: dict with title, subtitle, description, format, page_count, price
- outline: complete table of contents
- chapters: list of chapter summaries (5-10 chapters)
- key_takeaways: main value points for each chapter
- worksheets_templates: additional resources to include
- cover_description: visual brief for cover design
- seo_metadata: title, description, keywords for sales page
- sample_content: first chapter or section full text
- suggested_bonuses: additional items to increase perceived value""",
            user_prompt=f"""Generate a complete digital product. Format: {kwargs.get('format', 'pdf')}.
Niche: {kwargs.get('niche', 'online business')}
Target Audience: {kwargs.get('audience', 'entrepreneurs')}
Product Type: {kwargs.get('product_type', 'guide')}

Create something people would happily pay for. Focus on:
1. Practical value (actionable, implementable)
2. Unique angle (not rehashing what's out there)
3. Professional quality (well-structured, well-written)
4. Complete package (everything the customer needs)

The product should be ready to sell on Gumroad."""
        )

        self.log_performance("product_generator", result)
        return result
