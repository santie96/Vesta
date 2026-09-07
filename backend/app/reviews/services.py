from .models import *
from app.database.connection import AsyncSession
from sqlalchemy import select, and_
from .schemas import SiteReviewCreateSchema, SiteReviewResponseSchema, PaginatedSiteReviewsResponse
from app.users.services import get_user_by_id
from sqlalchemy.orm import selectinload
from app.core.exceptions.exceptions import PageNotFoundException


async def get_site_reviews_service(
    db: AsyncSession, 
    page: int, 
    limit: int,
    review_rating: float | None
) -> PaginatedSiteReviewsResponse:
    """
    Get paginated site reviews
    """
    
    conditions = [SiteReview.rating >= review_rating] if review_rating is not None else []
    
    site_reviews = (
        await db.execute(
            select(SiteReview)
            .where(and_(*conditions))
            .order_by(SiteReview.created_at.desc(), SiteReview.id.desc())
            .offset((page - 1) * limit)
            .limit(limit)
            .options(
                selectinload(SiteReview.user)
            )
        )
    ).scalars().all()
    
    total_items = (
        await db.execute(
            select(func.count())
            .select_from(SiteReview)
            .where(SiteReview.rating >= review_rating or review_rating is None)
        )
    ).scalar().one()
    
    total_pages = (total_items + limit - 1) // limit
    
    if 0 < total_pages < page:
        raise PageNotFoundException(f"Page {page} not found")
    
    return PaginatedSiteReviewsResponse(
        total_items=total_items,
        total_pages=total_pages,
        items_per_page=limit,
        prev_page=page - 1 if page > 1 else None,
        next_page=page + 1 if page < total_pages else None,
        current_page=page,
        items=[SiteReviewResponseSchema.model_validate(review) for review in site_reviews],
    )
    
    

async def create_site_review_service(
    current_user_id: int, 
    payload: SiteReviewCreateSchema, 
    db: AsyncSession
) -> SiteReviewResponseSchema:
    """
    Create a new site review
    """
    
    user = await get_user_by_id(current_user_id, db)
    
    site_review = SiteReview(
        rating=payload.rating,
        message=payload.message,
        user=user
    )
    
    db.add(site_review)
    await db.commit()
    await db.refresh(site_review, ["user"])
    
    return SiteReviewResponseSchema.model_validate(site_review)