from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import json
from app.models.response import ApiResponse

class ResponseWrapperMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)

        if response.status_code >= 400:
            return response

        body = b""
        async for chunk in response.body_iterator:
            body += chunk

        try:
            data = json.loads(body.decode())
        except:
            data = body.decode()

        wrapped = ApiResponse(
            success=True,
            message="OK",
            data=data
        ).dict()

        return JSONResponse(
            status_code=response.status_code,
            content=wrapped
        )
