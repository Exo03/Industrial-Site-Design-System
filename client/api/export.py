import httpx
import os
from client.config.settings import API_BASE_URL

async def export_json(project_id: int, token: str, output_dir: str = ".") -> str:
    try:
        async with httpx.AsyncClient(base_url = API_BASE_URL) as client:
            response = await client.get(
                f"/api/v1/project/{project_id}/export/json",
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()

            filepath = os.path.join(output_dir, f"project_{project_id}.json")#добавлено с помощью ии
            with open(filepath, "w", encoding ="utf-8") as f:#добавлено с помощью ии
                f.write(response.text)
            return filepath


    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            raise ValueError("Сессия истекла. Войдите снова.")
        elif e.response.status_code == 404:
            raise ValueError("Проект не найден или доступ запрещён")
        else:
            raise ValueError("Не удалось экспортировать проект в JSON")

    except httpx.ConnectTimeout:
        raise ValueError("Сервер не отвечает. Проверьте подключение.")
    except httpx.RequestError:
        raise ValueError("Ошибка сети. Попробуйте позже.")


async def export_svg(project_id: int, token: str, output_dir: str = ".") -> str:
    try:
        async with httpx.AsyncClient(base_url=API_BASE_URL, timeout=15.0) as client:
            response = await client.get(
                f"/api/v1/project/{project_id}/export/svg",
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()

            filepath = os.path.join(output_dir, f"project_{project_id}.svg")
            with open(filepath, "wb") as f:
                f.write(response.content)
            return filepath

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            raise ValueError("Сессия истекла. Войдите снова.")
        elif e.response.status_code == 404:
            raise ValueError("Проект не найден или доступ запрещён")
        else:
            raise ValueError("Не удалось экспортировать проект в SVG")

    except httpx.ConnectTimeout:
        raise ValueError("Сервер не отвечает. Проверьте подключение.")
    except httpx.RequestError:
        raise ValueError("Ошибка сети. Попробуйте позже.")

async def export_pdf(project_id: int, token: str, output_dir: str = ".") -> str:
    try:
        async with httpx.AsyncClient(base_url=API_BASE_URL, timeout=15.0) as client:
            response = await client.get(
                f"/api/v1/project/{project_id}/export/pdf",
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()

            filepath = os.path.join(output_dir, f"project_{project_id}.pdf")
            with open(filepath, "wb") as f:
                f.write(response.content)
            return filepath

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            raise ValueError("Сессия истекла. Войдите снова.")
        elif e.response.status_code == 404:
            raise ValueError("Проект не найден или доступ запрещён")
        else:
            raise ValueError("Не удалось экспортировать проект в PDF")

    except httpx.ConnectTimeout:
        raise ValueError("Сервер не отвечает. Проверьте подключение.")
    except httpx.RequestError:
        raise ValueError("Ошибка сети. Попробуйте позже.")
