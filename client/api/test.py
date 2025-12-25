# client/api/test_elements.py
import asyncio
from client.api.auth import login
from client.api.elements import add_elements, get_project_elements

async def test_elements():
    print("🔹 Шаг 1: Логин")
    try:
        # 🔑 ЗАМЕНИ НА СВОЙ РЕАЛЬНЫЙ ЛОГИН И ПАРОЛЬ!
        USERNAME = "testuser"
        PASSWORD = "123456"

        token_data = await login(USERNAME, PASSWORD)
        token = token_data["access_token"]
        print("✅ Успешный вход. Токен получен.")

    except Exception as e:
        print(f"❌ Ошибка логина: {e}")
        return

    print("\n🔹 Шаг 2: Добавление элемента")
    try:
        # 🔢 ЗАМЕНИ НА СУЩЕСТВУЮЩИЙ project_id (например, 1)
        PROJECT_ID = 1

        element = await add_elements(
            project_id=PROJECT_ID,
            element_type_id=1,
            x=100,
            y=200,
            width=10,
            length=15,
            token=token
        )
        print(f"✅ Элемент создан. ID: {element['id']}")

    except Exception as e:
        print(f"❌ Ошибка добавления элемента: {e}")
        return

    print("\n🔹 Шаг 3: Получение элементов проекта")
    try:
        elements = await get_project_elements(PROJECT_ID, token)
        print(f"✅ Получено элементов: {len(elements)}")
        for el in elements[-2:]:
            print(f"   • ID: {el['id']}, ({el['x']}, {el['y']}), {el['width']}×{el['length']}")

    except Exception as e:
        print(f"❌ Ошибка получения элементов: {e}")

if __name__ == "__main__":
    asyncio.run(test_elements())