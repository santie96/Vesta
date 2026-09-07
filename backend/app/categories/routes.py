from fastapi import APIRouter, Depends, status, Query
from app.database.connection import get_db, AsyncSession
from .schemas import *
from .services import *

router = APIRouter(
    prefix="/categories",
    tags=["Categories & Subcategories"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=CategoryPaginatedSchema)
async def get_categories(
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
):
    """
    Get paginated categories
    """
    
    return await get_categories_service(db, page, limit) 


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CategorySchema)
async def create_new_category(
    payload: CategoryCreateSchema,
    db: AsyncSession = Depends(get_db), 
):
    """
    Create a new category 
    
    (AUTHENTICATION AND ADMIN ROLE REQUIRED)
    """
    
    return await create_category_service(db, payload)


@router.patch("/{category_id}", status_code=status.HTTP_200_OK, response_model=CategorySchema)
async def update_category(
    payload: CategoryUpdateSchema,    
    category_id: int, 
    db: AsyncSession = Depends(get_db),
):
    """
    Update a category 
    
    (AUTHENTICATION AND ADMIN ROLE REQUIRED)
    """
    
    return await update_category_service(db, payload, category_id)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete permanently a category and every related subcategory and product
    
    (AUTHENTICATION AND ADMIN ROLE REQUIRED)
    """
    
    return await delete_category_service(db, category_id)


@router.get("/subcategories", status_code=status.HTTP_200_OK, response_model=SubCategoryPaginatedSchema)
async def get_subcategories(
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
):
    """
    Get paginated subcategories
    """
    
    return await get_subcategories_service(db, page, limit)


@router.get("/subcategories/{subcategory_id}", status_code=status.HTTP_200_OK, response_model=SubCategorySchema)
async def get_subcategory_details(
    subcategory_id: int, 
    db: AsyncSession = Depends(get_db)
):
    """
    Get subcategory details with relationships
    """
    
    return await get_subcategory_details_service(db, subcategory_id)


@router.post("/subcategories", status_code=status.HTTP_201_CREATED, response_model=SubCategorySchema)
async def create_new_subcategory(
    payload: SubCategoryCreateSchema,
    db: AsyncSession = Depends(get_db), 
):
    """
    Create a new subcategory 
    
    (AUTHENTICATION AND ADMIN ROLE REQUIRED)
    """
    
    return await create_subcategory_service(db, payload)


@router.patch("/subcategories/{subcategory_id}", status_code=status.HTTP_200_OK, response_model=SubCategorySchema)
async def update_subcategory(
    payload: SubCategoryUpdateSchema,    
    subcategory_id: int, 
    db: AsyncSession = Depends(get_db),
):
    """
    Update a subcategory 
    
    (AUTHENTICATION AND ADMIN ROLE REQUIRED)
    """
    
    return await update_subcategory_service(db, subcategory_id, payload)


@router.delete("/subcategories/{subcategory_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subcategory(subcategory_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete permanently a subcategory and every related product
    
    (AUTHENTICATION AND ADMIN ROLE REQUIRED)
    """
    
    return await delete_subcategory_service(db, subcategory_id)