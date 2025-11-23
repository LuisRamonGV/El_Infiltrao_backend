from fastapi import APIRouter, HTTPException
from app.models.category_model import ( CategoryCreate, CategoryResponse, CategoryUpdate )
from app.repositories.category_repository import CategoryRepository

router = APIRouter()

@router.get("", response_model=list[CategoryResponse])
def get_categories():
    """Obtiene todas las categorías."""
    return CategoryRepository.get_all()

@router.post("", response_model=CategoryResponse)
def add_category(data: CategoryCreate):
    """Crea una nueva categoría."""
    try:
        return CategoryRepository.create(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: str):
    """Obtiene una categoría por ID."""
    category = CategoryRepository.get(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: str, data: CategoryUpdate):
    try:
        updated = CategoryRepository.update(category_id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    if not updated:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated

@router.delete("/{category_id}", response_model=CategoryResponse)
def delete_category(category_id: str):
    deleted = CategoryRepository.delete(category_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Category not found")

    return deleted