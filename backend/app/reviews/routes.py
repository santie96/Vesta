from fastapi import APIRouter, Depends, status, Query
from app.database.connection import get_db, AsyncSession
from .services import *
from .schemas import *

router = APIRouter(
    prefix="/reviews",
    tags=["Site Reviews"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=PaginatedSiteReviewsResponse)
async def get_site_reviews(
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    review_rating: float | None = None
):
    """
    Get paginated site reviews
    """
    
    return await get_site_reviews_service(db, page, limit, review_rating)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=SiteReviewResponseSchema)
async def create_site_reviews(
    current_user_id: int, 
    payload: SiteReviewCreateSchema, 
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new site review
    
    (AUTHENTICATION AND USER ROLE REQUIRED)
    """
    
    return await create_site_review_service(current_user_id, payload, db)