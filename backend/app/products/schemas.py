from pydantic import BaseModel, field_validator, field_serializer, computed_field
from datetime import datetime
from .models import TargetKey
from re import match
from app.core.schemas import SyncModelORM, BasePaginatedResponse
from app.categories.schemas import CategorySchema, SubCategorySchema
from app.reviews.schemas import BaseReviewCreateSchema, BaseReviewUpdateSchema
from app.users.schemas import UserReviewResponseSchema

# ====================================
# PRODUCT
# ====================================

class ProductSchema(SyncModelORM):
    id: int
    title: str
    subtitle: str
    description: str
    slug: str
    price_cents: float
    sale_percent: int
    new_arrivals: bool
    image_url: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    sub_category: SubCategorySchema
    variants: list[ProductVariantSchema]
    reviews: list[ProductReviewResponseSchema]

    @field_serializer("price_cents")
    def serialize_price_cents(self, value: int) -> float:
        """
        Serialize the price_cents field as a float in API Response
        """
        return value / 100

    @computed_field
    @property
    def category(self) -> CategorySchema:
        return CategorySchema.model_validate(self.sub_category.category)

class ProductCreateSchema(BaseModel):
    title: str
    subtitle: str
    description: str
    price_cents: int
    sale_percent: int | None = None
    new_arrivals: bool | None = None
    image_url: str
    
    sub_category_id: int

    variant: ProductVariantNestedCreateSchema
    
    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError(
                "title cannot be empty"
            )
        
        if len(value) > 100:
            raise ValueError(
                "title length must be less than 100 characters"
            )
        return value
    
    @field_validator("subtitle")
    @classmethod
    def validate_subtitle(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError(
                "subtitle cannot be empty"
            )
        
        if len(value) > 100:
            raise ValueError(
                "subtitle length must be less than 100 characters"
            )
        return value
    
    
    @field_validator("sale_percent")
    @classmethod
    def validate_sale_percent(cls, value: int) -> int:
        if value < 0 or value > 100:
            raise ValueError("sale_percent must be between 0 and 100")
        return value
    
    @field_validator("price_cents")
    @classmethod
    def validate_price_cents(cls, value: int) -> int:
        if value < 0:
            raise ValueError("price_cents must be positive value")
        return value

    
    @field_validator("sub_category_id")
    @classmethod
    def validate_sub_category_id(cls, value: int) -> int:
        if value < 0:
            raise ValueError("sub_category_id must be positive value")
        return value    
    
    
class ProductUpdateSchema(ProductCreateSchema):
    title: str | None = None
    subtitle: str | None = None
    description: str | None = None
    price_cents: int | None = None
    sale_percent: int | None = None
    new_arrivals: bool | None = None
    image_url: str | None = None
    is_active: bool | None = None
    
    sub_category_id: int | None = None
    
    variant: ProductVariantUpdateSchema
    
    
class PaginatedProductResponse(BasePaginatedResponse):
    items: list[ProductSchema]

# ====================================
# PRODUCT VARIANT
# ====================================

class ProductVariantSchema(SyncModelORM):
    id: int
    size: str
    color_name: str
    color_hex: str
    target_key: TargetKey
    stock: int
    
    @field_validator("stock")
    @classmethod
    def validate_stock(cls, value: int) -> int:
        if value < 0:
            raise ValueError("stock must be greater than 0")
        return value


class ProductVariantNestedCreateSchema(BaseModel):
    size: str
    color_name: str
    color_hex: str
    target_key: TargetKey
    stock: int    
        
    @field_validator("stock")
    @classmethod
    def validate_stock(cls, value: int) -> int:
        if value < 0:
            raise ValueError("stock must be positive value")
        return value
    
    @field_validator("color_hex")
    @classmethod
    def validate_color_hex(cls, value: str) -> str:
        if not match(r"^#([A-Fa-f0-9]{6})$", value):
            raise ValueError("color_hex must be a valid hex color code")
        return value
    
    
class ProductVariantCreateSchema(ProductVariantNestedCreateSchema):
    product_id: int

    @field_validator("product_id")
    @classmethod
    def validate_product_id(cls, value: int) -> int:
        if value < 0:
            raise ValueError("product_id must be positive value")
        return value
    
class ProductVariantUpdateSchema(ProductVariantCreateSchema):
    id: int
    
    size: str | None = None
    color_name: str | None = None
    color_hex: str | None = None
    target_key: TargetKey | None = None
    stock: int | None = None
    
    @field_validator("id")
    @classmethod
    def validate_id(cls, value: int) -> int:
        if value < 0:
            raise ValueError("id must be positive value")
        return value
    
    
class ProductReviewCreateSchema(BaseReviewCreateSchema):
    pass
    
    
class ProductReviewUpdateSchema(BaseReviewUpdateSchema):
    pass

class ProductReviewResponseSchema(SyncModelORM):
    id: int
    rating: float
    message: str
    created_at: datetime
    updated_at: datetime
    
    user: UserReviewResponseSchema
    
    
class PaginatedProductReviewsResponse(BasePaginatedResponse):
    items: list[ProductReviewResponseSchema]