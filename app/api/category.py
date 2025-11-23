from fastapi import APIRouter
from app.core.firebase import db
from pydantic import BaseModel

router = APIRouter()

@router.get("/")
async def get_categories():
    docs = db.collection("categories").stream()
    categories = [{ "id": doc.id, **doc.to_dict() } for doc in docs]
    return categories

class Category(BaseModel):
    name: str
    description: str | None = None

@router.post("/")
async def add_category(category: Category):
    doc_ref = db.collection("categories").document()
    doc_ref.set(category.dict())
    return { "id": doc_ref.id, **category.dict() }


@router.get("/{category_id}")
async def get_category(category_id: str):
    doc = db.collection("categories").document(category_id).get()
    if not doc.exists:
        return {"error": "not found"}
    return {"id": doc.id, **doc.to_dict()}

@router.delete("/{category_id}")
async def delete_category(category_id: str):
    db.collection("categories").document(category_id).delete()
    return { "status": "deleted" }

