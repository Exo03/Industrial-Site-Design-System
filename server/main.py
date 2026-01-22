from fastapi import FastAPI
from server.api.v1.endpoints import users, elements, projects, auth, element_types
from server.db.session import engine
from server.db.base import Base
from server.api.middleware import RequestLoggingMiddleware

# Создание приложение
app = FastAPI(
    title="Industrial Site Design System API",
    description="API для управления проектами и элементами",
    version="1.0.0",
    docs_url="/api/docs",        
    redoc_url="/api/redoc",      
    openapi_url="/api/openapi.json"
)

# Подключение middelware
app.add_middleware(RequestLoggingMiddleware)

# Подключение маршрутов из эндпоинтов
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(elements.router, prefix="/api/v1", tags=["elements"])
app.include_router(projects.router, prefix="/api/v1", tags=["projects"])
app.include_router(element_types.router, prefix="/api/v1", tags=["element_types"])

#app.include_router(admin.router, prefix="/api/v1", tags=["admin"])
