from fastapi import FastAPI, HTTPException
from app.api.category import router as category_router
from app.middleware.response_middleware import ResponseWrapperMiddleware
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from app.models.response import ApiResponse
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def test_firestore():
    return {"status": "Ok",
            "message": "Server started"}

app.include_router(category_router, prefix="/category", tags=["Category"])
app.add_middleware(ResponseWrapperMiddleware)

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ApiResponse(
            success=False,
            message=exc.detail,
            data=None
        ).dict()
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content=ApiResponse(
            success=False,
            message="Validation error",
            data=exc.errors()
        ).dict()
    )