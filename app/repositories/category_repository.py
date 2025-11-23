from app.core.firebase import db
from app.models.category_model import CategoryCreate, CategoryUpdate

class CategoryRepository:

    @staticmethod
    def get_all():
        docs = db.collection("categories").stream()
        return [{ "id": d.id, **d.to_dict()} for d in docs]
    
    @staticmethod
    def get(category_id: str):
        doc = db.collection("categories").document(category_id).get()
        if not doc.exists:
            return None
        return { "id": doc.id, **doc.to_dict() }

    @staticmethod
    def create(data: CategoryCreate):
        exists = db.collection("categories") \
                   .where("name", "==", data.name) \
                   .limit(1) \
                   .stream()
        if list(exists):
            raise ValueError("Category name already exists")
        ref = db.collection("categories").document()
        ref.set(data.model_dump())
        return { "id": ref.id, **data.model_dump() }

    @staticmethod
    def update(category_id: str, data: CategoryUpdate):
        doc_ref = db.collection("categories").document(category_id)
        existing_doc = doc_ref.get()
        if not existing_doc.exists:
            return None
        if data.name:
            exists = db.collection("categories") \
                       .where("name", "==", data.name) \
                       .limit(1) \
                       .stream()
            for doc in exists:
                if doc.id != category_id:
                    raise ValueError("Category name already exists")
        update_data = data.model_dump(exclude_none=True)
        doc_ref.update(update_data)
        return { "id": category_id, **doc_ref.get().to_dict() }

    @staticmethod
    def delete(category_id: str):
        ref = db.collection("categories").document(category_id)
        doc = ref.get()
        if not doc.exists:
            return None

        deleted = {"id": doc.id, **doc.to_dict()}
        ref.delete()
        return deleted
