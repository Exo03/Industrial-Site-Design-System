import httpx
import json
from client.config.settings import API_BASE_URL

async def get_current_user(token: str) -> dict:
    async with httpx.AsyncClient(base_url=API_BASE_URL,  timeout = 15.0) as client:
        response = await client.get(
            "/api/v1/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        response.raise_for_status()
        return response.json()

async def delete_user(password: str, token: str) -> bool:
    async with httpx.AsyncClient(base_url=API_BASE_URL, timeout=15.0) as client:
        response = await client.request(
            "DELETE",
            "/api/v1/delete_user",
            content=json.dumps({"password": password}),
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )
        response.raise_for_status()
        return True