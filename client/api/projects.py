import httpx
from client.config.settings import API_BASE_URL

async def create_project(name: str, description: str, width: int, length: int, token: str) -> dict:
    try:
        async with httpx.AsyncClient(base_url = API_BASE_URL,  timeout = 15.0) as client:
            response = await client.post(
                "/api/v1/create_project",
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

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            raise ValueError("Сессия истекла. Войдите снова.")
        else:
            raise ValueError("Не удалось создать проект")
    except (httpx.ConnectTimeout, httpx.RequestError):
        raise ValueError("Сервер недоступен. Проверьте подключение")

async def get_user_projects(token: str) -> list:
    try:
        async with httpx.AsyncClient(base_url = API_BASE_URL,  timeout = 15.0) as client:
            response = await client.get(
                f"/api/v1/user_projects",
                headers = {"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            return response.json()

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            raise ValueError("Сессия истекла. Войдите снова.")
        else:
            raise ValueError("Не удалось загрузить проекты")
    except (httpx.ConnectTimeout, httpx.RequestError):
        raise ValueError("Сервер недоступен. Проверьте подключение")

async def delete_project(project_id: int, token: str) -> bool:
    try:
        async with httpx.AsyncClient(base_url = API_BASE_URL,  timeout = 15.0) as client:
            response = await client.delete(
                f"/api/v1/delete_project/{project_id}",
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            return True

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            raise ValueError("Сессия истекла. Войдите снова.")
        elif e.response.status_code == 404:
            raise ValueError("Проект не найден или доступ запрещен")
        else:
            raise ValueError("Не удалось удалить проект")
    except (httpx.ConnectTimeout, httpx.RequestError):
        raise ValueError("Сервер недоступен. Проверьте подключение")


async def rename_project(project_id: int, name: str,description: str, width: int, length: int, token: str) -> dict:
    try:
        async with httpx.AsyncClient(base_url = API_BASE_URL,  timeout = 15.0) as client:
            response = await client.put(
                f"/api/v1/rename_project/{project_id}",
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

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            raise ValueError("Сессия истекла. Войдите снова.")
        elif e.response.status_code == 404:
            raise ValueError("Проект не найден или доступ запрещен")
        else:
            raise ValueError("Не удалось обновить проект")
    except (httpx.ConnectTimeout, httpx.RequestError):
        raise ValueError("Сервер недоступен. Проверьте подключение")

async def get_project(project_id: int, token: str) -> dict:
    try:
        async with httpx.AsyncClient(base_url = API_BASE_URL,  timeout = 15.0) as client:
            response = await client.get(
                f"/api/v1/project/{project_id}",
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            return response.json()

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            raise ValueError("Сессия истекла. Войдите снова.")
        elif e.response.status_code == 404:
            raise ValueError("Проект не найден или доступ запрещен")
        else:
            raise ValueError("Не удалось загрузить проект")
    except (httpx.ConnectTimeout, httpx.RequestError):
        raise ValueError("Сервер недоступен. Проверьте подключение")

async def resize_project(project_id: int, width: int, length: int, token: str) -> dict:
    try:
        async with httpx.AsyncClient(base_url=API_BASE_URL, timeout=15.0) as client:
            response = await client.put(
                "/api/v1/resize_project",
                json={
                    "id": project_id,
                    "width": width,
                    "length": length
                },
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            return response.json()

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            raise ValueError("Сессия истекла. Войдите снова.")
        elif e.response.status_code == 403:
            raise ValueError("Доступ запрещен")
        elif e.response.status_code == 404:
            raise ValueError("Проект не найден")
        else:
            raise ValueError("Не удалось изменить размер проекта")
    except (httpx.ConnectTimeout, httpx.RequestError):
        raise ValueError("Сервер недоступен. Проверьте подключение")