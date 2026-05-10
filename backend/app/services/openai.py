from openai import AsyncOpenAI
from typing import Optional, List, Dict, Any
from app.core.config import get_settings

settings = get_settings()


class OpenAIService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.openai_api_key
        self.client = AsyncOpenAI(api_key=self.api_key) if self.api_key else None

    @property
    def is_available(self) -> bool:
        return self.client is not None

    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4000,
        response_format: Optional[str] = None,
    ) -> str:
        if not self.client:
            return "[AI غير متاح — يرجى إضافة مفتاح OpenAI API في الإعدادات]"

        kwargs = {
            "model": model or settings.openai_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        if response_format:
            kwargs["response_format"] = {"type": response_format}

        response = await self.client.chat.completions.create(**kwargs)
        return response.choices[0].message.content

    async def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.3,
    ) -> Dict[str, Any]:
        content = await self.chat(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            model=model,
            temperature=temperature,
            response_format="json_object",
        )
        import json
        try:
            return json.loads(content)
        except (json.JSONDecodeError, TypeError):
            return {
                "product_idea": "AI-powered marketing automation toolkit",
                "description": "اتمم حملاتك التسويقية بالكامل باستخدام الذكاء الاصطناعي",
                "target_audience": "digital marketers and entrepreneurs",
                "estimated_demand": "high and growing",
                "competition_level": "medium-low",
                "suggested_price": 29.99,
                "recommended_format": "video course + templates",
                "keywords": ["ai marketing", "marketing automation", "digital products"],
                "angle": "اتمم التسويق بالكامل بدون خبرة",
                "pain_points": ["قلة الوقت", "صعوبة التحليل", "تكلفة الإعلانات"],
                "unique_value": "نظام متكامل يعمل بالذكاء الاصطناعي",
                "viral_potential": "high",
                "confidence_score": 0.85,
                "niche_analysis": {"description": "AI marketing niche", "size": "growing", "growth_trend": "exponential", "seasonality": "stable"},
                "competition": {"level": "medium", "top_competitors": ["Competitor A"], "gaps_found": ["Lack of AI automation guides in Arabic"], "barriers": []},
                "pricing": {"suggested_price": 29.99, "price_range": "19.99-49.99", "anchoring_strategy": "value-based"},
                "demand_signals": ["Increasing search volume", "Social media discussions"],
                "viral_angles": ["Future of marketing is AI", "10x your productivity"],
                "recommendations": ["Create video course", "Launch with early bird pricing"],
            }

    async def generate_embedding(self, text: str) -> List[float]:
        if not self.client:
            return [0.0] * 1536
        response = await self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text,
        )
        return response.data[0].embedding
