# server/api/middleware.py
import time
import logging
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.concurrency import iterate_in_threadpool
from typing import Union

# Настройка логгера
logger = logging.getLogger("request-logger")
logger.setLevel(logging.INFO)

# Обработчик для вывода в консоль (можно заменить на файл)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware для логирования всех входящих HTTP-запросов и исходящих ответов."""

    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.time()
        client_host = request.client.host if request.client else "unknown"
        logger.info(f"Request: {request.method} {request.url.path} from {client_host}")

        try:
            response: Response = await call_next(request)

            process_time = time.time() - start_time
            logger.info(
                f"Response: {response.status_code} for {request.method} {request.url.path} "
                f"({process_time:.3f}s)"
            )
            return response

        except Exception as e:
            process_time = time.time() - start_time
            logger.error(
                f"Error: {type(e).__name__}: {str(e)} "
                f"during {request.method} {request.url.path} ({process_time:.3f}s)"
            )
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal Server Error"},
            )