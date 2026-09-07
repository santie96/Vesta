from fastapi import APIRouter, Depends, status, Query
from app.database.connection import get_db, AsyncSession
from .schemas import *
from .services import *
from typing import Literal
from .models import TargetKey

router = APIRouter(
    prefix="/products",
    tags=["Products, Variants & Product Reviews"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=PaginatedProductResponse)
async def get_products(
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    new_arrivals: bool | None = None,
    category_id: int | None = None,
    color_name: str | None = None,
    size: str | None = None,
    target_key: TargetKey | None = None,
    sort: Literal[
        "price_asc", 
        "price_desc", 
        "created_at_asc", 
        "created_at_desc"
        ] | None = None,
    review_rating: float | None = None
    ):
    """
    Get paginated products with category, subcategory, variants and reviews
    
    Can be filtered by query params
    
    Can update default pagination params
    """
    return await get_products_service(
        db, 
        page, 
        limit,
        new_arrivals,
        category_id,
        color_name,
        size,
        target_key,
        sort,
        review_rating
        )


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProductSchema)
async def create_new_product(
    payload: ProductCreateSchema,
    db: AsyncSession = Depends(get_db), 
):
    """
    Create a new product with its variant
    
    Format alidation on request body
    
    Validation image url (check if image is reachable)
    
    (AUTHENTICATION AND ADMIN ROLE REQUIRED)
    """
    
    return await create_product_service(db, payload)


@router.get("/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductSchema)
async def get_product_details(
    product_id: int, 
    db: AsyncSession = Depends(get_db)
):
    """
    Get product details with relationships
    """
    
    return await get_product_details_service(db, product_id)


@router.patch("/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductSchema)
async def update_product(
    payload: ProductUpdateSchema,    
    product_id: int, 
    db: AsyncSession = Depends(get_db),
):
    """
    Update a product
    
    This endpoint can also be used to update a product variant
    
    (AUTHENTICATION AND ADMIN ROLE REQUIRED)
    """
    
    return await update_product_service(db, product_id, payload)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete permanently a product and every related variant
    
    (AUTHENTICATION AND ADMIN ROLE REQUIRED)
    """
    
    return await delete_product_service(db, product_id)

@router.post("/variants", status_code=status.HTTP_201_CREATED, response_model=ProductVariantSchema)
async def create_new_variant(
    payload: ProductVariantCreateSchema,
    db: AsyncSession = Depends(get_db), 
):
    """
    Create a new variant for a product
    
    (AUTHENTICATION AND ADMIN ROLE REQUIRED)
    """
    
    return await create_variant_service(db, payload)


@router.delete("/variants/{variant_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_variant(variant_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete permanently a variant
    
    (AUTHENTICATION AND ADMIN ROLE REQUIRED)
    """
    
    return await delete_variant_service(db, variant_id)


@router.get("/{product_id}/reviews", status_code=status.HTTP_200_OK, response_model=PaginatedProductReviewsResponse)
async def get_product_reviews(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    """
    Get paginated product reviews
    """
    
    return await get_product_reviews_service(db, product_id, page, limit)


@router.post(
    "/{product_id}/reviews", 
    status_code=status.HTTP_201_CREATED,
    response_model=ProductReviewResponseSchema
)
async def create_product_reviews(
    current_user_id: int,
    product_id: int, 
    payload: ProductReviewCreateSchema, 
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new product review for a specific product
    
    (AUTHENTICATION AND USER ROLE REQUIRED)
    """
    
    return await create_product_review_service(current_user_id,product_id, payload, db)

@router.patch("/reviews/{review_id}", status_code=status.HTTP_200_OK, response_model=ProductReviewResponseSchema)
async def update_product_review(
    payload: ProductReviewUpdateSchema,    
    review_id: int, 
    db: AsyncSession = Depends(get_db),
):
    """
    Update a product review
    
    (AUTHENTICATION AND USER ROLE REQUIRED)
    """
    
    return await update_product_review_service(db, review_id, payload)


@router.delete("/reviews/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_review(review_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete permanently a product review
    
    (AUTHENTICATION REQUIRED)
    """
    
    return await delete_product_review_service(db, review_id)