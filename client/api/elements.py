import httpx
from client.config.settings import API_BASE_URL

async def add_elements(project_id: int, element_type_id: int, x: int, y: int, width: int, length:int,title:str, color:str, token:str) -> dict:
    async with httpx.AsyncClient(base_url = API_BASE_URL,  timeout = 15.0) as client:
        response = await client.post(
            "/api/v1/add_element",
            json = {
                "project_id": project_id,
                "element_type_id": element_type_id,
                "x" : x,
                "y" : y,
                "width": width,
                "length": length,
                "title": title,
                "color": color
            },
            headers = {"Authorization": f"Bearer {token}"}#добавлено с помощью ии
        )
    response.raise_for_status()#добавлено с помощью ии
    return response.json()

async def get_project_elements(project_id: int, token:str) -> list:#использовано ии
    async with httpx.AsyncClient(base_url = API_BASE_URL,  timeout = 15.0) as client:
        response = await client.get(
            f"/api/v1/project/{project_id}/elements",
            headers={"Authorization": f"Bearer {token}"})
    response.raise_for_status()
    return response.json()

async def delete_element(element_id: int, token: str) -> bool:
    async with httpx.AsyncClient(base_url=API_BASE_URL,  timeout = 15.0) as client:
        response = await client.delete(
            f"/api/v1/delete_element/{element_id}",
            headers={"Authorization": f"Bearer {token}"}#добавлено с помощью ии
        )
    response.raise_for_status()
    return True


async def move_element(id:int, x: int, y: int, token: str) -> dict:
    async with httpx.AsyncClient(base_url=API_BASE_URL,  timeout = 15.0) as client:
        response = await client.put(
            f"/api/v1/move_element",
            json = {
                "id": id,
                "x": x,
                "y": y,
            },
            headers = {"Authorization": f"Bearer {token}"}
        )
        response.raise_for_status()
        return response.json()

async def resize_element(id:int, width: int, length: int, token: str) -> dict:
    async with httpx.AsyncClient(base_url=API_BASE_URL,  timeout = 15.0) as client:
        response = await client.put(
            f"/api/v1/resize_element",
            json = {
                "id": id,
                "width": width,
                "length": length,
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        response.raise_for_status()
        return response.json()


async def get_elements(element_id:int, token:str) -> dict:
    async with httpx.AsyncClient(base_url = API_BASE_URL,  timeout = 15.0) as client:
        response = await client.get(
            f"/api/v1/element/{element_id}",
            headers = {"Authorization": f"Bearer {token}"}
        )
        response.raise_for_status()
        return response.json()

async def recolor_element(id: int, color: str, token: str) -> dict:
    async with httpx.AsyncClient(base_url=API_BASE_URL, timeout=15.0) as client:
        response = await client.put(
            "/api/v1/recolor_element",
            json={"id": id, "color": color},
            headers={"Authorization": f"Bearer {token}"}
        )
        response.raise_for_status()
        return response.json()


async def rename_element(id: int, title: str, token: str) -> dict:
    async with httpx.AsyncClient(base_url=API_BASE_URL, timeout=15.0) as client:
        response = await client.put(
            "/api/v1/rename_element",
            json={"id": id, "title": title},
            headers={"Authorization": f"Bearer {token}"}
        )
        response.raise_for_status()
        return response.json()

