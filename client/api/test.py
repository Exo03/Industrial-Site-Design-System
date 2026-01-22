# client/api/test_full.py
import asyncio
import uuid
from client.api.auth import register, login
from client.api.projects import (
    create_project, get_user_projects, get_project,
    rename_project, delete_project
)
from client.api.elements import (
    add_elements, get_project_elements, get_elements,
    move_element, resize_element, delete_element
)
from client.api.users import get_current_user
from client.api.element_types import get_element_types, get_element_type

async def test_full_workflow():
    # === 1. РЕГИСТРАЦИЯ И ВХОД ===
    unique = str(uuid.uuid4())[:6]
    email = f"test_{unique}@example.com"
    username = f"testuser_{unique}"
    password = "secure_pass_123"

    print("🔹 1. Регистрация")
    try:
        await register(email, username, password)
        print("✅ Пользователь создан")
    except Exception as e:
        if "already exists" not in str(e):
            print(f"❌ Ошибка регистрации: {e}")
            return

    print("\n🔹 2. Вход")
    try:
        token_data = await login(username, password)
        token = token_data["access_token"]
        print("✅ Успешный вход")
    except Exception as e:
        print(f"❌ Ошибка логина: {e}")
        return

    # === 2. ПРОФИЛЬ ===
    print("\n🔹 3. Получение профиля")
    try:
        profile = await get_current_user(token)
        print(f"✅ Профиль: {profile['username']}")
    except Exception as e:
        print(f"⚠️ Не удалось загрузить профиль: {e}")

    # === 3. КАТАЛОГ ТИПОВ ОБОРУДОВАНИЯ ===
    print("\n🔹 4. Загрузка каталога типов оборудования")
    try:
        types = await get_element_types()
        print(f"✅ Найдено типов: {len(types)}")
        if not types:
            print("⚠️ Каталог пуст — тест невозможен")
            return
        element_type_id = types[0]["id"]
        print(f"   → Используем тип: {types[0]['title']} (ID: {element_type_id})")
    except Exception as e:
        print(f"❌ Ошибка загрузки каталога: {e}")
        return

    # === 4. РАБОТА С ПРОЕКТАМИ ===
    project_id = None
    try:
        print("\n🔹 5. Создание проекта")
        project = await create_project(
            name="Тестовый проект",
            description="Для полного теста",
            width=100,
            length=200,
            token=token
        )
        project_id = project["id"]
        print(f"✅ Проект ID: {project_id}")

        print("\n🔹 6. Список проектов")
        projects = await get_user_projects(token)
        print(f"✅ Всего проектов: {len(projects)}")

        print("\n🔹 7. Получение проекта по ID")
        proj_detail = await get_project(project_id, token)
        print(f"✅ Проект: {proj_detail['name']}")

        print("\n🔹 8. Переименование проекта")
        renamed = await rename_project(
            project_id=project_id,
            name="Обновлённый проект",
            description=proj_detail["description"],
            width=proj_detail["width"],
            length=proj_detail["length"],
            token=token
        )
        print(f"✅ Новое имя: {renamed['name']}")

    except Exception as e:
        print(f"❌ Ошибка с проектами: {e}")
        if project_id:
            try:
                await delete_project(project_id, token)
            except:
                pass
        return

    # === 5. РАБОТА С ЭЛЕМЕНТАМИ ===
    element_id = None
    try:
        print("\n🔹 9. Добавление элемента")
        element = await add_elements(
            project_id=project_id,
            element_type_id=element_type_id,
            x=10,
            y=20,
            width=5,      # ← размеры задаются явно
            length=8,
            title="Тестовый агрегат",
            color="#4A90E2",
            token=token
        )
        element_id = element["id"]
        print(f"✅ Элемент ID: {element_id}")

        print("\n🔹 10. Список элементов проекта")
        elements = await get_project_elements(project_id, token)
        print(f"✅ Элементов в проекте: {len(elements)}")

        print("\n🔹 11. Получение элемента по ID")
        elem_detail = await get_elements(element_id, token)
        print(f"✅ Элемент: {elem_detail['title']} @ ({elem_detail['x']}, {elem_detail['y']})")

        # 🔸 Получаем тип оборудования через элемент (без размеров!)
        print("\n🔹 12. Получение типа оборудования через элемент")
        type_info = await get_element_type(element_id, token)
        print(f"✅ Тип: {type_info['title']}")
        if type_info.get("description"):
            print(f"   → Описание: {type_info['description']}")

        print("\n🔹 13. Перемещение элемента")
        moved = await move_element(id=element_id, x=30, y=40, token=token)
        print(f"✅ Перемещён на: ({moved['x']}, {moved['y']})")

        print("\n🔹 14. Изменение размера")
        resized = await resize_element(id=element_id, width=7, length=10, token=token)
        print(f"✅ Новый размер: {resized['width']} × {resized['length']}")

    except Exception as e:
        print(f"❌ Ошибка с элементами: {e}")
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

    # === 6. ОЧИСТКА ===
    try:
        print("\n🔹 15. Удаление элемента")
        await delete_element(element_id, token)
        print("✅ Элемент удалён")

        print("\n🔹 16. Удаление проекта")
        await delete_project(project_id, token)
        print("✅ Проект удалён")

    except Exception as e:
        print(f"⚠️ Ошибка при очистке: {e}")

    print("\n🎉 Полный цикл тестирования завершён успешно!")

if __name__ == "__main__":
    asyncio.run(test_full_workflow())