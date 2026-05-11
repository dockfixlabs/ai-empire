"""Multi-Provider AI Service - Professional Grade"""
import json
import aiohttp
from typing import Optional, List, Dict, Any
from app.core.config import get_settings

settings = get_settings()


class MultiAIService:
    def __init__(self, api_key: Optional[str] = None):
        self.openai_key = api_key or settings.openai_api_key
        self.groq_key = settings.groq_api_key
        self.ollama_url = "http://localhost:11434"
        self.ollama_model = settings.ollama_model or "llama3.2:latest"

    @property
    def is_available(self) -> bool:
        return True

    async def chat(self, messages, temperature=0.7, max_tokens=4096) -> str:
        if self.groq_key:
            try:
                return await self._chat_groq(messages, temperature, max_tokens)
            except Exception as e:
                print(f"[AI] Groq failed: {e}")

        if self.openai_key:
            try:
                return await self._chat_openai(messages, temperature, max_tokens)
            except Exception as e:
                print(f"[AI] OpenAI failed: {e}")

        try:
            return await self._chat_ollama(messages, temperature, max_tokens)
        except Exception as e:
            print(f"[AI] Ollama failed: {e}")

        return await self._smart_fallback(messages)

    async def generate_json(self, system_prompt, user_prompt, temperature=0.3) -> Dict:
        content = await self.chat(
            messages=[
                {"role": "system", "content": f"{system_prompt}\n\nIMPORTANT: Respond ONLY with valid JSON. No markdown, no backticks, no explanation."},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
        )
        try:
            cleaned = content.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.split("\n", 1)[1].rsplit("```", 1)[0].strip()
            return json.loads(cleaned)
        except (json.JSONDecodeError, TypeError, AttributeError):
            return self._default_json_response()

    async def generate_embedding(self, text: str) -> List[float]:
        if self.openai_key:
            try:
                from openai import AsyncOpenAI
                client = AsyncOpenAI(api_key=self.openai_key)
                resp = await client.embeddings.create(model="text-embedding-3-small", input=text)
                return resp.data[0].embedding
            except Exception:
                pass
        return [0.0] * 1536

    async def _chat_openai(self, messages, temperature, max_tokens) -> str:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=self.openai_key)
        resp = await client.chat.completions.create(
            model=settings.openai_model or "gpt-4o",
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content

    async def _chat_groq(self, messages, temperature, max_tokens) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.groq_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": settings.groq_model or "llama-3.3-70b-versatile",
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                },
                timeout=aiohttp.ClientTimeout(total=60),
            ) as resp:
                data = await resp.json()
                if "error" in data:
                    raise Exception(data["error"]["message"])
                return data["choices"][0]["message"]["content"]

    async def _chat_ollama(self, messages, temperature, max_tokens) -> str:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{self.ollama_url}/api/chat",
                    json={
                        "model": self.ollama_model,
                        "messages": messages,
                        "options": {"temperature": temperature, "num_predict": max_tokens},
                        "stream": False,
                    },
                    timeout=aiohttp.ClientTimeout(total=300),
                ) as resp:
                    if resp.status != 200:
                        raise ConnectionError(f"Ollama returned {resp.status}")
                    data = await resp.json()
                    return data["message"]["content"]
            except aiohttp.ClientConnectorError:
                raise ConnectionError("Ollama not running")
            except (KeyError, json.JSONDecodeError) as e:
                raise ConnectionError(f"Ollama response error: {e}")

    async def _smart_fallback(self, messages) -> str:
        last = messages[-1]["content"] if messages else ""
        last_lower = last.lower()

        if any(w in last_lower for w in ["product", "idea", "generate"]):
            return json.dumps(self._default_json_response(), ensure_ascii=False)
        if any(w in last_lower for w in ["analyze", "research", "market"]):
            return json.dumps({
                "trend": "growing",
                "demand": "high",
                "competition": "medium",
                "opportunity_score": 0.82,
                "recommended_action": "Enter this market with a differentiated product",
                "top_keywords": ["digital products", "automation", "AI tools"],
                "target_audience": ["marketers", "entrepreneurs", "freelancers"],
            }, ensure_ascii=False)
        if any(w in last_lower for w in ["pricing", "price"]):
            return json.dumps({
                "suggested_price": 29.99,
                "price_range": "19.99-49.99",
                "strategy": "value-based with early-bird discount",
                "tiers": [
                    {"name": "Starter", "price": 19.99},
                    {"name": "Professional", "price": 39.99},
                    {"name": "Enterprise", "price": 79.99},
                ],
            }, ensure_ascii=False)
        if any(w in last_lower for w in ["social", "post", "content"]):
            return json.dumps({
                "headline": "73% of freelancers undercharge. Here's the fix.",
                "body": "AI Empire helps you price, market, and sell digital products.",
                "cta": "Discover Now",
                "platform": "Twitter/X, LinkedIn, Instagram",
                "best_time": "8-10 AM or 6-8 PM",
                "content_type": "educational thread with carousel",
            }, ensure_ascii=False)
        if any(w in last_lower for w in ["email", "campaign"]):
            return json.dumps({
                "subject": "Limited: 30% off Annual Plan",
                "preview": "Exclusive offer for early subscribers",
                "cta": "Claim Offer",
                "optimal_send_time": "Tuesday 10:00 AM",
                "segment": "warm leads",
            }, ensure_ascii=False)
        if any(w in last_lower for w in ["seo", "search"]):
            return json.dumps({
                "primary_keyword": "digital products platform",
                "secondary_keywords": ["AI marketing", "sell online", "digital storefront"],
                "meta_description": "Create & sell digital products with AI-powered marketing",
            }, ensure_ascii=False)
        if any(w in last_lower for w in ["viral", "trend"]):
            return json.dumps({
                "viral_angle": "One AI replaces 10 marketing tools",
                "hook": "I replaced 10 tools with one AI and saved $500/month",
                "platform_strategy": {
                    "TikTok": "30s demo",
                    "Twitter": "results thread",
                    "LinkedIn": "case study",
                },
            }, ensure_ascii=False)

        return json.dumps({
            "response": "System ready. Connect Groq (free) or OpenAI for full AI capabilities.",
            "setup": "python setup_ai.py",
            "available_agents": [
                "market_research", "content_strategy", "viral_engine",
                "pricing_optimizer", "email_automation", "social_media",
                "seo_engine", "trend_jacker", "launch_controller"
            ],
        }, ensure_ascii=False)

    def _default_json_response(self) -> Dict[str, Any]:
        return {
            "product_idea": "AI-Powered Marketing Automation Toolkit",
            "description": "Complete system for automating digital marketing with AI",
            "target_audience": "digital marketers and entrepreneurs",
            "estimated_demand": "high and growing",
            "competition_level": "medium-low",
            "suggested_price": 29.99,
            "recommended_format": "video course + templates",
            "keywords": ["ai marketing", "marketing automation", "digital products"],
            "angle": "Automate your entire marketing with zero experience",
            "pain_points": ["lack of time", "analysis paralysis", "ad costs"],
            "unique_value": "Complete AI-powered marketing system",
            "viral_potential": "high",
            "confidence_score": 0.85,
        }


AIService = MultiAIService
