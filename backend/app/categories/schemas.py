from pydantic import BaseModel, field_validator
from app.core.schemas import SyncModelORM

# ====================================
# CATEGORY
# ====================================
class CategorySchema(SyncModelORM):
    id: int
    name: str
    slug: str
    is_active: bool

class CategoryPaginatedSchema(BaseModel):
    total_items: int
    total_pages: int
    items_per_page: int
    prev_page: int | None
    current_page: int
    next_page: int | None
    items: list[CategorySchema]
    
class CategoryCreateSchema(BaseModel):
    name: str
    
    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError(
                "name cannot be empty"
            )
        
        if len(value) > 100:
            raise ValueError(
                "name length must be less than 100 characters"
            )
        return value


class CategoryUpdateSchema(CategoryCreateSchema):
    name: str | None = None
    is_active: bool | None = None

# ====================================
# SUBCATEGORY
# ====================================

class SubCategorySchema(SyncModelORM):
    id: int
    name: str
    slug: str
    is_active: bool
    
    category: CategorySchema


class SubCategoryPaginatedSchema(BaseModel):
    total_items: int
    total_pages: int
    items_per_page: int
    prev_page: int | None
    current_page: int
    next_page: int | None
    items: list[SubCategorySchema]

class SubCategoryCreateSchema(BaseModel):
    name: str
    category_id: int
    
    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError(
                "name cannot be empty"
            )
        
        if len(value) > 100:
            raise ValueError(
                "name length must be less than 100 characters"
            )
        return value


class SubCategoryUpdateSchema(SubCategoryCreateSchema):
    name: str | None = None
    is_active: bool | None = None
    category_id: int | None = None
    
