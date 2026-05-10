import httpx
from typing import Optional, Dict
from app.core.config import get_settings

settings = get_settings()

AUTH_URL = "https://gumroad.com/oauth/authorize"
TOKEN_URL = "https://api.gumroad.com/oauth/token"
API_BASE = "https://api.gumroad.com/v2"


class GumroadOAuth:
    def __init__(self, client_id: str = None, client_secret: str = None):
        self.client_id = client_id or settings.gumroad_client_id
        self.client_secret = client_secret or settings.gumroad_client_secret

    def get_authorization_url(self, redirect_uri: str, state: str = None) -> str:
        params = {
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": "edit_products view_sales view_profile",
        }
        if state:
            params["state"] = state
        from urllib.parse import urlencode
        return f"{AUTH_URL}?{urlencode(params)}"

    async def exchange_code(self, code: str, redirect_uri: str) -> Optional[Dict]:
        async with httpx.AsyncClient() as client:
            r = await client.post(TOKEN_URL, data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": redirect_uri,
            })
            if r.status_code == 200:
                return r.json()
            return None

    async def refresh_token(self, refresh_token: str) -> Optional[Dict]:
        async with httpx.AsyncClient() as client:
            r = await client.post(TOKEN_URL, data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": refresh_token,
                "grant_type": "refresh_token",
            })
            if r.status_code == 200:
                return r.json()
            return None

    async def test_connection(self, access_token: str) -> bool:
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{API_BASE}/user", params={"access_token": access_token})
            return r.status_code == 200
