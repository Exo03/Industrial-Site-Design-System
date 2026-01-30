import httpx
from client.config.settings import API_BASE_URL

async def get_element_type(element_id: int, token: str) -> dict:
    try:
        async with httpx.AsyncClient(base_url= API_BASE_URL,  timeout = 15.0) as client:
            response = await client.get(
                f"/api/v1/element_type/{element_id}",
                headers={"Authorization": f"Bearer {token}"},
            )
            response.raise_for_status()
            return response.json()

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            raise ValueError("Сессия истекла. Войдите снова.")
        elif e.response.status_code == 403:
            raise ValueError("Доступ запрещён")
        elif e.response.status_code == 404:
            raise ValueError("Элемент или его тип не найден")
        else:
            raise ValueError("Не удалось загрузить тип оборудования")
    except (httpx.ConnectTimeout, httpx.RequestError):
        raise ValueError("Сервер недоступен. Проверьте подключение")

async def get_element_types() -> list:
    try:
        async with httpx.AsyncClient(base_url= API_BASE_URL,  timeout = 15.0) as client:
            response = await client.get(
                f"/api/v1/all_element_types"
            )
            response.raise_for_status()
            return response.json()

    except httpx.HTTPStatusError as e:
        raise ValueError("Не удалось загрузить каталог оборудования")
    except (httpx.ConnectTimeout, httpx.RequestError):
        raise ValueError("Сервер недоступен. Проверьте подключение")

