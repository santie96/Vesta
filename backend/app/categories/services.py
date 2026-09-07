from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload
from .schemas import *
from .models import Category, SubCategory
from app.core.exceptions.exceptions import PageNotFoundException
from .exceptions import *
from app.core.utils import create_slug


async def _get_category_by_id(db: AsyncSession, category_id: int) -> Category:
    category = (
        await db.execute(
            select(Category).where(Category.id == category_id)
        )
    ).scalar_one_or_none()
    
    if category is None:
        raise CategoryNotFoundException(f"Category with id {category_id} not found")
    
    return category


async def get_categories_service(db: AsyncSession, page: int, limit: int) -> CategoryPaginatedSchema:
    """
    Get paginated categories
    """
    
    categories = (
        await db.execute(
            select(Category)
            .where(Category.is_active == True)
            .offset((page - 1) * limit)
            .limit(limit)
        )
    ).scalars().all()
    
    total_items = (
        await db.execute(
            select(func.count())
            .where(Category.is_active == True)
        )
    ).scalars().one()
    
    total_pages = (total_items + limit - 1) // limit
    
    if 0 < total_pages < page:
        raise PageNotFoundException(f"Page {page} not found")

    return CategoryPaginatedSchema(
        total_items=total_items,
        total_pages=total_pages,
        items_per_page=limit,
        prev_page=page - 1 if page > 1 else None,
        current_page=page,
        next_page=page + 1 if page < total_pages else None,
        items=[CategorySchema.model_validate(category) for category in categories]
    )
    

async def create_category_service(db: AsyncSession, payload: CategoryCreateSchema) -> CategorySchema:
    """
    Create a new category
    """
    
    existing_category = (
        await db.execute(
            select(Category).where(Category.name == payload.name.lower())
        )
    ).scalar_one_or_none()
    
    if existing_category is not None:
        raise CategoryAlreadyExistsException(f"Category with name {payload.name} already exists")
    
    category = Category(
        name=payload.name,
        slug=create_slug(payload.name)
    )
    
    db.add(category)
    await db.commit()
    await db.refresh(category)
    
    return CategorySchema.model_validate(category)


async def update_category_service(
    db: AsyncSession, 
    paylaod: CategoryUpdateSchema, 
    category_id: int
) -> CategorySchema:
    
    existing_category = await _get_category_by_id(db, category_id)
    
    if existing_category is None:
        raise CategoryNotFoundException(f"Category with id {category_id} not found")
    
    update_data = paylaod.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(existing_category, key, value)
    
    await db.commit()
    await db.refresh(existing_category)
    
    return CategorySchema.model_validate(existing_category)


async def delete_category_service(db: AsyncSession, category_id: int) -> None:
    """
    Delete permanently a category and every related subcategory and product
    """
    
    existing_category = await _get_category_by_id(db, category_id)
    
    if existing_category is None:
        raise CategoryNotFoundException(f"Category with id {category_id} not found")
    
    await db.delete(existing_category)
    await db.commit()
    
    
    
# ==============================
# SUBCATEGORIES
# ==============================

async def _get_subcategory_by_id(db: AsyncSession, subcategory_id: int) -> SubCategory:
    subcategory = (
        await db.execute(
            select(SubCategory)
            .where(SubCategory.id == subcategory_id)
            .options(selectinload(SubCategory.category))
        )
    ).scalar_one_or_none()
    
    if subcategory is None:
        raise SubCategoryNotFoundException(f"SubCategory with id {subcategory_id} not found")
    
    return subcategory

async def get_subcategories_service(db: AsyncSession, page: int, limit: int) -> SubCategoryPaginatedSchema:
    """
    Get paginated subcategories
    """
    
    conditions = [
        SubCategory.is_active == True,
        SubCategory.category.has(Category.is_active == True)
    ]
    
    subcategories = (
        await db.execute(
            select(SubCategory)
            .where(and_(*conditions))
            .offset((page - 1) * limit)
            .limit(limit)
            .options(selectinload(SubCategory.category))
        )
    ).scalars().all()
    
    total_items = (
        await db.execute(
            select(func.count())
            .where(and_(*conditions))
        )
    ).scalars().one()
    
    total_pages = (total_items + limit - 1) // limit
    
    if 0 < total_pages < page:
        raise PageNotFoundException(f"Page {page} not found")

    return SubCategoryPaginatedSchema(
        total_items=total_items,
        total_pages=total_pages,
        items_per_page=limit,
        prev_page=page - 1 if page > 1 else None,
        current_page=page,
        next_page=page + 1 if page < total_pages else None,
        items=[SubCategorySchema.model_validate(subcategory) for subcategory in subcategories]
    )
    

async def get_subcategory_details_service(db: AsyncSession, subcategory_id: int) -> SubCategorySchema:
    """
    Get subcategory details with relationships
    """
    
    subcategory = await _get_subcategory_by_id(db, subcategory_id)
    
    if subcategory is None:
        raise SubCategoryNotFoundException(f"SubCategory with id {subcategory_id} not found")
    
    return SubCategorySchema.model_validate(subcategory)


async def create_subcategory_service(
    db: AsyncSession, 
    payload: SubCategoryCreateSchema
) -> SubCategorySchema:
    """
    Create a new subcategory 
    """
    
    existing_category = await _get_category_by_id(db, payload.category_id)
    
    if existing_category is None:
        raise CategoryNotFoundException(f"Category with id {payload.category_id} not found")
    
    existing_subcategory = (
        await db.execute(
            select(SubCategory).where(SubCategory.name == payload.name.lower())
        )
    ).scalar_one_or_none()
    
    if existing_subcategory is not None:
        raise SubCategoryAlreadyExistsException(f"SubCategory with name {payload.name} already exists")
    
    subcategory = SubCategory(
        name=payload.name,
        slug=create_slug(existing_category.slug, payload.name),
        category=existing_category
    )
    
    db.add(subcategory)
    await db.commit()
    await db.refresh(subcategory)
    
    return SubCategorySchema.model_validate(subcategory)


async def update_subcategory_service(
    db: AsyncSession, 
    subcategory_id: int, 
    payload: SubCategoryUpdateSchema
) -> SubCategorySchema:
    
    existing_subcategory = await _get_subcategory_by_id(db, subcategory_id)
    
    if existing_subcategory is None:
        raise SubCategoryNotFoundException(f"SubCategory with id {subcategory_id} not found")
    
    existing_category = await _get_category_by_id(db, payload.category_id)
    
    if existing_category is None:
        raise CategoryNotFoundException(f"Category with id {payload.category_id} not found")
    
    update_data = payload.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(existing_subcategory, key, value)
    
    new_slug = create_slug(existing_category.slug, existing_subcategory.name)
    
    is_valid_slug = (
        await db.execute(
            select(SubCategory).where(SubCategory.slug == new_slug)
        )
    ).scalar_one_or_none()
    
    if is_valid_slug is not None and is_valid_slug.id != subcategory_id:
        raise SubCategorySlugAlreadyExistsException(f"Slug {new_slug} already exists")
    
    await db.commit()
    await db.refresh(existing_subcategory)
    
    return SubCategorySchema.model_validate(existing_subcategory)


async def delete_subcategory_service(db: AsyncSession, subcategory_id: int) -> None:
    """
    Delete permanently a subcategory and every related product
    """
    
    existing_subcategory = await _get_subcategory_by_id(db, subcategory_id)
    
    await db.delete(existing_subcategory)
    await db.commit()