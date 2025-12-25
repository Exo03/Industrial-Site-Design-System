import httpx
from client.config.settings import API_BASE_URL

async def add_elements(project_id: int, element_type_id: int, x: int, y: int, width: int, length:int, token:str) -> dict:
    async with httpx.AsyncClient(base_url = API_BASE_URL) as client:
        response = await client.post(
            "/api/v1/elements/add_element",
            json = {
                "project_id": project_id,
                "element_type_id": element_type_id,
                "x" : x,
                "y" : y,
                "width": width,
                "length": length
            },
            headers = {"Authorization": f"Bearer {token}"}#добавлено с помощью ии
        )
    response.raise_for_status()
    return response.json()

async def get_project_elements(project_id: int, element_type_id: int, x: int, y: int, width: int, length:int, token:str) -> dict:
    async with httpx.AsyncClient(base_url = API_BASE_URL) as client:
        response = await client.get(
            "/api/v1/elements/project/{project_id}/elements",
            headers={"Authorization": f"Bearer {token}"})
    response.raise_for_status()
    return response.json()

