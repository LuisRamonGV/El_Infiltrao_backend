from fastapi import FastAPI
from app.api.category import router as category_router


app = FastAPI()

@app.get("/")
def test_firestore():
    return {"status": "Ok",
            "message": "Server started"}

app.include_router(category_router, prefix="/category", tags=["Category"])

