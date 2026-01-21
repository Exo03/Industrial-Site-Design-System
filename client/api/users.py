import httpx
from client.config.settings import API_BASE_URL

async def get_current_user(token: str) -> dict:
    async with httpx.AsyncClient(base_url=API_BASE_URL) as client:
        response = await client.get(
            "/api/v1/users/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        response.raise_for_status()
        return response.json()

async def delete_user(password: str, token: str) -> bool:
    async with httpx.AsyncClient(base_url=API_BASE_URL) as client:
        response = await client.delete(
            "/api/v1/users/delete_user",
            json={"password": password},
            headers={"Authorization": f"Bearer {token}"}
        )
        response.raise_for_status()
        return True