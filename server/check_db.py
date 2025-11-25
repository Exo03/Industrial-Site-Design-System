import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from config.settings import settings

async def check_database():
    # Создаём движок
    engine = create_async_engine(settings.DATABASE_URL, echo=False)

    try:
        # Проверка подключения
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        print("✅ Успешное подключение к базе данных")

        # Выводим содержимое таблиц
        async with engine.connect() as conn:
            # Таблица users
            print("\n=== Таблица users ===")
            result = await conn.execute(text("SELECT id, username, email FROM users"))
            users = result.fetchall()
            if users:
                for user in users:
                    print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}")
            else:
                print("Таблица пуста")

            # Таблица projects
            print("\n=== Таблица projects ===")
            result = await conn.execute(text("SELECT id, name, owner_id, description FROM projects"))
            projects = result.fetchall()
            if projects:
                for proj in projects:
                    print(f"ID: {proj.id}, Name: {proj.name}, Owner ID: {proj.owner_id}, Description: {proj.description}")
            else:
                print("Таблица пуста")

            # Таблица elements
            print("\n=== Таблица elements ===")
            result = await conn.execute(text("SELECT id, element_type_id, x, y, rotation, project_id FROM elements"))
            elements = result.fetchall()
            if elements:
                for el in elements:
                    print(f"ID: {el.id}, Type: {el.element_type_id}, Coords: ({el.x}, {el.y}, Rotation: {el.rotation}), "
                          f"Project ID: {el.project_id}")
            else:
                print("Таблица пуста")

    except Exception as e:
        print(f"❌ Ошибка подключения или запроса: {e}")
    finally:
        await engine.dispose()

asyncio.run(check_database())