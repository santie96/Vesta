from app.database.connection import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, Float, DateTime, func, ForeignKey
from datetime import datetime 

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.users.models import User


class SiteReview(Base):
    __tablename__ = "site_reviews"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )
    
    # relationship with user model [MANY TO ONE]
    # ondelete="SET NULL"
    # if user is deleted, the review is not deleted
    # leave the review user reference empty (unknown)
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    user: Mapped["User"] = relationship("User", back_populates="site_reviews")