import httpx
from client.config.settings import API_BASE_URL

async def get_element_type(element_id: int, token: str) -> dict:
    async with httpx.AsyncClient(base_url= API_BASE_URL,  timeout = 15.0) as client:
        response = await client.get(
            f"/api/v1/element_type/{element_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        response.raise_for_status()
        return response.json()

async def get_element_types() -> list:
    async with httpx.AsyncClient(base_url= API_BASE_URL,  timeout = 15.0) as client:
        response = await client.get(
            f"/api/v1/all_element_types"
        )
        response.raise_for_status()
        return response.json()
