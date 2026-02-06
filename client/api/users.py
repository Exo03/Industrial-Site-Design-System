import httpx
import json
from client.config.settings import API_BASE_URL

async def get_current_user(token: str) -> dict:
    try:
        async with httpx.AsyncClient(base_url=API_BASE_URL,  timeout = 15.0) as client:
            response = await client.get(
                "/api/v1/me",
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            return response.json()

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            raise ValueError("Сессия истекла. Войдите снова.")
        else:
            raise ValueError("Не удалось загрузить профиль")
    except (httpx.ConnectTimeout, httpx.RequestError):
        raise ValueError("Сервер недоступен. Проверьте подключение")

async def delete_user(password: str, token: str) -> bool:
    try:
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

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            raise ValueError("Сессия истекла. Войдите снова.")
        elif e.response.status_code == 400:
            raise ValueError("Неверный пароль")
        else:
            raise ValueError("Не удалось удалить аккаунт")
    except (httpx.ConnectTimeout, httpx.RequestError):
        raise ValueError("Сервер недоступен. Проверьте подключение")
