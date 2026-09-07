from pydantic import BaseModel
from datetime import datetime

class RateLimitError(BaseModel):
    error: str
    unlock_at: datetime
    
