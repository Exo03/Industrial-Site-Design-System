import httpx
from client.config.settings import API_BASE_URL

async def add_elements(project_id: int, element_type_id: int, x: int, y: int, width: int, length:int,title:str, color:str, token:str) -> dict:
    try:
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

    except httpx.HTTPStatusError as e:#добавлено с помощью ии
        if e.response.status_code == 401:
            raise ValueError("Сессия истекла. Войдите снова.")
        elif e.response.status_code == 400:
            raise ValueError("Проект не найден или доступ запрещён")
        else:
            raise ValueError("Не удалось добавить элемент")
    except (httpx.ConnectTimeout, httpx.RequestError):
        raise ValueError("Сервер недоступен. Проверьте подключение")

async def get_project_elements(project_id: int, token:str) -> list:#использовано ии
    try:
        async with httpx.AsyncClient(base_url = API_BASE_URL,  timeout = 15.0) as client:
            response = await client.get(
                f"/api/v1/project/{project_id}/elements",
                headers={"Authorization": f"Bearer {token}"})
            response.raise_for_status()
            return response.json()

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            raise ValueError("Сессия истекла. Войдите снова.")
        elif e.response.status_code == 404:
            raise ValueError("Проект не найден или доступ запрещён")
        else:
            raise ValueError("Не удалось загрузить элементы")
    except (httpx.ConnectTimeout, httpx.RequestError):
        raise ValueError("Сервер недоступен. Проверьте подключение")

async def delete_element(element_id: int, token: str) -> bool:
    try:
        async with httpx.AsyncClient(base_url=API_BASE_URL,  timeout = 15.0) as client:
            response = await client.delete(
                f"/api/v1/delete_element/{element_id}",
                headers={"Authorization": f"Bearer {token}"}#добавлено с помощью ии
            )
            response.raise_for_status()
            return True

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            raise ValueError("Сессия истекла. Войдите снова.")
        elif e.response.status_code == 404:
            raise ValueError("Элемент не найден")
        elif e.response.status_code == 403:
            raise ValueError("Доступ запрещён")
        else:
            raise ValueError("Не удалось удалить элемент")
    except (httpx.ConnectTimeout, httpx.RequestError):
        raise ValueError("Сервер недоступен. Проверьте подключение")


async def move_element(id:int, x: int, y: int, token: str) -> dict:
    try:
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

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            raise ValueError("Сессия истекла. Войдите снова.")
        elif e.response.status_code == 404:
            raise ValueError("Элемент не найден")
        elif e.response.status_code == 403:
            raise ValueError("Доступ запрещён")
        else:
            raise ValueError("Не удалось переместить элемент")
    except (httpx.ConnectTimeout, httpx.RequestError):
        raise ValueError("Сервер недоступен. Проверьте подключение")

async def resize_element(id:int, width: int, length: int, token: str) -> dict:
    try:
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

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            raise ValueError("Сессия истекла. Войдите снова.")
        elif e.response.status_code == 404:
            raise ValueError("Элемент не найден")
        elif e.response.status_code == 403:
            raise ValueError("Доступ запрещён")
        else:
            raise ValueError("Не удалось изменить размер")
    except (httpx.ConnectTimeout, httpx.RequestError):
        raise ValueError("Сервер недоступен. Проверьте подключение")


async def get_elements(element_id:int, token:str) -> dict:
    try:
        async with httpx.AsyncClient(base_url = API_BASE_URL,  timeout = 15.0) as client:
            response = await client.get(
                f"/api/v1/element/{element_id}",
                headers = {"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            return response.json()

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            raise ValueError("Сессия истекла. Войдите снова.")
        elif e.response.status_code == 404:
            raise ValueError("Элемент не найден")
        elif e.response.status_code == 403:
            raise ValueError("Доступ запрещён")
        else:
            raise ValueError("Не удалось загрузить элемент")
    except (httpx.ConnectTimeout, httpx.RequestError):
        raise ValueError("Сервер недоступен. Проверьте подключение")

async def recolor_element(id: int, color: str, token: str) -> dict:
    try:
        async with httpx.AsyncClient(base_url=API_BASE_URL, timeout=15.0) as client:
            response = await client.put(
                "/api/v1/recolor_element",
                json={"id": id, "color": color},
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            return response.json()

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            raise ValueError("Сессия истекла. Войдите снова.")
        elif e.response.status_code == 404:
            raise ValueError("Элемент не найден")
        elif e.response.status_code == 403:
            raise ValueError("Доступ запрещён")
        else:
            raise ValueError("Не удалось изменить цвет")
    except (httpx.ConnectTimeout, httpx.RequestError):
        raise ValueError("Сервер недоступен. Проверьте подключение")


async def rename_element(id: int, title: str, token: str) -> dict:
    try:
        async with httpx.AsyncClient(base_url=API_BASE_URL, timeout=15.0) as client:
            response = await client.put(
                "/api/v1/rename_element",
                json={"id": id, "title": title},
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            return response.json()

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            raise ValueError("Сессия истекла. Войдите снова.")
        elif e.response.status_code == 404:
            raise ValueError("Элемент не найден")
        elif e.response.status_code == 403:
            raise ValueError("Доступ запрещён")
        else:
            raise ValueError("Не удалось переименовать элемент")
    except (httpx.ConnectTimeout, httpx.RequestError):
        raise ValueError("Сервер недоступен. Проверьте подключение")

