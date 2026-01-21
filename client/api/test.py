# client/api/test_elements.py #cделано с  помощью ии
import asyncio
from client.api.auth import login
from client.api.projects import create_project, delete_project
from client.api.elements import (
    add_elements,
    get_project_elements,
    get_elements,
    move_element,
    resize_element,
    delete_element
)

async def test_elements():
    # 🔑 Авторизация
    USERNAME = "test_user_12345"
    PASSWORD = "secure_password_123"

    print("🔹 Шаг 1: Вход в систему")
    try:
        token_data = await login(USERNAME, PASSWORD)
        token = token_data["access_token"]
        print("✅ Успешный вход")
    except Exception as e:
        print(f"❌ Ошибка логина: {e}")
        return

    project_id = None
    element_id = None

    try:
        # Создаём проект
        print("\n🔹 Шаг 2: Создание проекта")
        project = await create_project(
            name="Проект для теста элементов",
            description="Тестовые элементы",
            width=500,
            length=300,
            token=token
        )
        project_id = project["id"]
        print(f"✅ Проект создан. ID: {project_id}")

        # Добавляем элемент
        print("\n🔹 Шаг 3: Добавление элемента")
        element = await add_elements(
            project_id=project_id,
            element_type_id=1,
            x=50,
            y=60,
            width=20,
            length=30,
            title="Насос",
            color="#33FF57",
            token=token
        )
        element_id = element["id"]
        print(f"✅ Элемент создан. ID: {element_id}, Название: {element['title']}")

        # Получаем список элементов
        print("\n🔹 Шаг 4: Получение всех элементов проекта")
        elements = await get_project_elements(project_id, token)
        print(f"✅ Найдено элементов: {len(elements)}")

        # Получаем один элемент
        print("\n🔹 Шаг 5: Получение одного элемента")
        single = await get_elements(element_id, token)
        print(f"✅ Элемент: {single['title']} @ ({single['x']}, {single['y']})")

        # Перемещаем
        print("\n🔹 Шаг 6: Перемещение элемента")
        moved = await move_element(id=element_id, x=100, y=120, token=token)
        print(f"✅ Перемещён на: ({moved['x']}, {moved['y']})")

        # Изменяем размер
        print("\n🔹 Шаг 7: Изменение размера")
        resized = await resize_element(id=element_id, width=25, length=35, token=token)
        print(f"✅ Новый размер: {resized['width']} × {resized['length']}")


    except Exception as e:
        print(f"❌ Ошибка при работе с элементами: {e}")
        # Очистка
        if element_id:
            try:
                await delete_element(element_id, token)
            except:
                pass
        if project_id:
            try:
                await delete_project(project_id, token)
            except:
                pass
        return

    try:
        # Удаляем элемент
        print("\n🔹 Шаг 10: Удаление элемента")
        await delete_element(element_id, token)
        print("✅ Элемент удалён")

        # Удаляем проект
        print("\n🔹 Шаг 11: Удаление проекта")
        await delete_project(project_id, token)
        print("✅ Проект удалён")

    except Exception as e:
        print(f"⚠️ Ошибка при очистке: {e}")

    print("\n🎉 Все операции с элементами завершены успешно!")

if __name__ == "__main__":
    asyncio.run(test_elements())