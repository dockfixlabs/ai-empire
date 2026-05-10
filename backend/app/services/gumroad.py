import httpx
from typing import Optional, Dict, Any, List
from app.core.config import get_settings

settings = get_settings()


class GumroadService:
    BASE_URL = "https://api.gumroad.com/v2"

    def __init__(self, access_token: Optional[str] = None):
        self.access_token = access_token or settings.gumroad_api_key
        self.client = httpx.AsyncClient(timeout=30.0)

    async def _request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        url = f"{self.BASE_URL}/{endpoint}"
        params = {"access_token": self.access_token} if self.access_token else {}

        response = await self.client.request(method, url, params=params, json=data)
        response.raise_for_status()
        return response.json()

    async def get_user(self) -> Dict:
        return await self._request("GET", "user")

    async def get_products(self) -> List[Dict]:
        result = await self._request("GET", "products")
        return result.get("products", [])

    async def get_product(self, product_id: str) -> Dict:
        result = await self._request("GET", f"products/{product_id}")
        return result.get("product", {})

    async def create_product(
        self,
        name: str,
        description: str,
        price: float,
        currency: str = "usd",
        file_url: Optional[str] = None,
        max_purchase_count: Optional[int] = None,
        preview_url: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> Dict:
        data = {
            "name": name,
            "description": description,
            "price": int(price * 100),
            "currency": currency,
            "customizable_price": "true" if max_purchase_count else "false",
            "require_shipping": "false",
        }
        if preview_url:
            data["preview_url"] = preview_url
        if tags:
            data["tags"] = ",".join(tags)

        result = await self._request("POST", "products", data)
        return result.get("product", {})

    async def update_product(self, product_id: str, **kwargs) -> Dict:
        result = await self._request("PUT", f"products/{product_id}", kwargs)
        return result.get("product", {})

    async def enable_product(self, product_id: str) -> Dict:
        return await self._request("PUT", f"products/{product_id}/enable")

    async def disable_product(self, product_id: str) -> Dict:
        return await self._request("PUT", f"products/{product_id}/disable")

    async def delete_product(self, product_id: str) -> Dict:
        return await self._request("DELETE", f"products/{product_id}")

    async def get_sales(self, product_id: Optional[str] = None) -> List[Dict]:
        endpoint = f"products/{product_id}/sales" if product_id else "sales"
        result = await self._request("GET", endpoint)
        return result.get("sales", [])

    async def get_subscribers(self) -> List[Dict]:
        result = await self._request("GET", "subscribers")
        return result.get("subscribers", [])

    async def get_licenses(self, product_id: str) -> List[Dict]:
        result = await self._request("GET", f"products/{product_id}/licenses")
        return result.get("licenses", [])

    async def generate_license(self, product_id: str, email: str) -> Dict:
        data = {"product_id": product_id, "email": email}
        result = await self._request("POST", "licenses", data)
        return result.get("license", {})

    async def validate_license(self, product_id: str, license_key: str) -> Dict:
        data = {"product_id": product_id, "license_key": license_key}
        result = await self._request("POST", "licenses/validate", data)
        return result.get("license", {})

    async def get_resource_subscriptions(self) -> List[Dict]:
        result = await self._request("GET", "resource_subscriptions")
        return result.get("resource_subscriptions", [])

    async def create_resource_subscription(self, webhook_url: str, resource_type: str = "sale") -> Dict:
        data = {
            "resource_type": resource_type,
            "webhook_url": webhook_url,
        }
        result = await self._request("POST", "resource_subscriptions", data)
        return result.get("resource_subscription", {})

    async def close(self):
        await self.client.aclose()
