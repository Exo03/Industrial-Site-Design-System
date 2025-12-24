import asyncio
from client.api.auth import register, login

async def test():
    try:
        print("Регистрация...")
        user = await register("test@a.ru", "testuser", "123456")
        print("✅ Успех:", user)

        print("Логин...")
        token_data = await login("testuser", "123456")
        print("✅ Токен:", token_data["access_token"])

    except Exception as e:
        print("❌ Ошибка:", e)

if __name__ == "__main__":
    asyncio.run(test())