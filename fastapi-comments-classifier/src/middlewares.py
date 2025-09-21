# src/middlewares.py
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from .exceptions import NotFoundError, BadRequestError

class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)

        except NotFoundError as e:
            return self._json_response(404, e.detail)
        
        except BadRequestError as e:
            return self._json_response(400, e.detail)
        
        except Exception as e:
            return self._json_response(500, "Error interno del servidor")

    def _json_response(self, status_code: int, message: str):
        return JSONResponse(
            status_code=status_code,
            content={"detail": message}
        )
