from pydantic import BaseModel, ConfigDict

class SyncModelORM(BaseModel):
    """
    Base class for Pydantic models to include the ORM model configuration and validation
    """
    
    model_config = ConfigDict(from_attributes=True)


class BasePaginatedResponse(BaseModel):
    total_items: int
    total_pages: int
    items_per_page: int
    prev_page: int | None
    current_page: int
    next_page: int | None
    