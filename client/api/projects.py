import httpx
from client.config.settings import API_BASE_URL

async def create_project(name: str, description: str, width: int, length: int, token: str) -> dict:
    async with httpx.AsyncClient(base_url = API_BASE_URL) as client:
        response = await client.post(
            "/api/v1/projects/create_project",
            json={
                "name": name,
                "description": description,
                "width": width,
                "length": length,
            },
            headers = {"Authorization": f"Bearer {token}"}
        )
    response.raise_for_status()
    return response.json()

async def get_user_projects(token: str) -> list:
    async with httpx.AsyncClient(base_url = API_BASE_URL) as client:
        response = await client.get(
            f"/api/v1/projects/user_projects",
            headers = {"Authorization": f"Bearer {token}"}
        )
        response.raise_for_status()
        return response.json()

async def delete_project(project_id: int, token: str) -> bool:
    async with httpx.AsyncClient(base_url = API_BASE_URL) as client:
        response = await client.delete(
            f"/api/v1/projects/delete_project/{project_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        response.raise_for_status()
        return True

async def rename_project(project_id: int, name: str,description: str, width: int, length: int, token: str) -> dict:
    async with httpx.AsyncClient(base_url = API_BASE_URL) as client:
        response = await client.put(
            f"/api/v1/projects/rename_project/{project_id}",
            json = {
                "name": name,
                "description": description,
                "width": width,
                "length": length
                },
            headers={"Authorization": f"Bearer {token}"},
        )
        response.raise_for_status()
        return response.json()

async def get_project(project_id: int, token: str) -> dict:
    async with httpx.AsyncClient(base_url = API_BASE_URL) as client:
        response = await client.get(
            f"/api/v1/projects/project/{project_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        response.raise_for_status()
        return response.json()