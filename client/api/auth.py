import httpx
from client.config.settings import API_BASE_URL

async def register(email: str, username: str, password: str) -> dict:
    try:
        async with httpx.AsyncClient(base_url = API_BASE_URL, timeout = 15.0) as client:
            response = await client.post(
                "/api/v1/register",
                json={
                    "email": email.strip(),
                    "username": username.strip(),
                    "password": password,
                }
            )
            response.raise_for_status()
            return response.json()

    except httpx.HTTPStatusError as e:#добавлено с помощью нейросети
        status_code = e.response.status_code
        try:
            error_detail = e.response.json().get("detail", "")
        except:
            error_detail = ""

        if status_code == 400:
                    if "email already exists" in error_detail:
                        raise ValueError("Пользователь с таким email уже существует")
                    elif "username already exists" in error_detail:
                        raise ValueError("Этот логин уже занят")
                    else:
                        raise ValueError("Некорректные данные при регистрации")
        else:
            raise ValueError("Неизвестная ошибка")

    except httpx.ConnectTimeout:
        raise ValueError("Сервер не отвечает. Проверьте подключение.")
    except httpx.RequestError:
        raise ValueError("Ошибка сети. Попробуйте позже.")

async def login(username: str, password: str) -> dict:
    try:
        async with httpx.AsyncClient(base_url = API_BASE_URL, timeout= 15.0) as client:
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
    except httpx.HTTPStatusError as e:
        status_code = e.response.status_code

        if status_code == 401:
            raise ValueError("Неверный логин или пароль")
        else:
            raise ValueError("Неизвестная ошибка")

    except httpx.ConnectTimeout:
        raise ValueError("Сервер не отвечает. Проверьте подключение.")
    except httpx.RequestError:
        raise ValueError("Ошибка сети. Попробуйте позже.")
