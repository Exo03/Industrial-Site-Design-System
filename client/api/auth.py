import httpx
from client.config.settings import API_BASE_URL

async def register(email: str, username: str, password: str) -> dict:
    async with httpx.AsyncClient(base_url = API_BASE_URL) as client:
        response = await client.post(
            "/api/v1/register",
            json={
                "email": email,
                "username": username,
                "password": password,
            }
        )
    response.raise_for_status()
    return response.json()

async def login(username: str, password: str) -> dict:
    async with httpx.AsyncClient(base_url = API_BASE_URL) as client:
        response = await client.post(
            "/api/v1/token",
            data={
                "username": username,
                "password": password,
                "grant_type" : "password"
            }
        )
    response.raise_for_status()
    return response.json()