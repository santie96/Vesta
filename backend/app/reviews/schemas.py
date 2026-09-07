from app.core.schemas import SyncModelORM
from pydantic import field_validator
from datetime import datetime
from app.users.schemas import UserReviewResponseSchema
from app.core.schemas import BasePaginatedResponse

class BaseReviewCreateSchema(SyncModelORM):
    rating: float
    message: str

    @field_validator("rating")
    @classmethod
    def validate_rating(cls, value: float) -> float:
        allowed_values = (1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5)
        if value not in allowed_values:
            raise ValueError(f"rating must be one of {allowed_values}")
        return value
    
    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError(
                "message cannot be empty"
            )
        
        if len(value) > 5000:
            raise ValueError(
                "message length must be less than 500 characters"
            )
        return value


class BaseReviewUpdateSchema(BaseReviewCreateSchema):
    rating: float | None = None
    message: str | None = None
    

class SiteReviewUpdateSchema(BaseReviewUpdateSchema): 
    pass

class SiteReviewCreateSchema(BaseReviewCreateSchema): 
    pass


class SiteReviewResponseSchema(SyncModelORM):
    id: int
    rating: float
    message: str
    created_at: datetime
    updated_at: datetime
    
    user: UserReviewResponseSchema
    

class PaginatedSiteReviewsResponse(BasePaginatedResponse):
    items: list[SiteReviewResponseSchema]
    