from app.database.connection import Base
from sqlalchemy import (
    String, 
    Enum as SQLAEnum, 
    DateTime, 
    func, 
    ForeignKey, 
    Boolean, 
    Text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum
from datetime import datetime

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.products.models import ProductReviews
    from app.reviews.models import SiteReview


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"


class User(Base):
    __tablename__  = "users"
    
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    surname: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    hash_pwd: Mapped[str] = mapped_column(String(300), nullable=False)
    gender: Mapped[Gender] = mapped_column(
        SQLAEnum(Gender),
        nullable=False,
        default=Gender.OTHER
    ) 
    
    role: Mapped[Role] = mapped_column(
        SQLAEnum(Role),
        nullable=False,
        default=Role.USER
    )
    
    birth_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None
    )
    
    telephone_number: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
        default=None
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    last_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )
    
    # relationship with addresses model [ONE TO MANY]
    addresses: Mapped[list["Address"]] = relationship(
        "Address", 
        back_populates="user", 
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    
    # relationship with product reviews model [ONE TO MANY]
    product_reviews: Mapped[list["ProductReviews"]] = relationship(
        "ProductReviews", 
        back_populates="user", 
        passive_deletes=True
    )

    # relationship with site reviews model [ONE TO MANY]
    site_reviews: Mapped[list["SiteReview"]] = relationship(
        "SiteReview", 
        back_populates="user", 
        passive_deletes=True
    )

class AddressType(str, Enum):
    BILLING = "billing"
    SHIPPING = "shipping"

class Address(Base):
    __tablename__ = "addresses"
    
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    
    type: Mapped[AddressType] = mapped_column(
        SQLAEnum(AddressType),
        nullable=True
    )
    
    via: Mapped[str] = mapped_column(String(100), nullable=True)
    city: Mapped[str] = mapped_column(String(100), nullable=True)
    cap: Mapped[str] = mapped_column(String(5), nullable=True)
    province: Mapped[str] = mapped_column(String(100), nullable=True)
    country: Mapped[str] = mapped_column(String(100), nullable=True)

    delivery_annotation: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    default: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )
    
    # relationship with user model [MANY TO ONE]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user: Mapped["User"] = relationship(
        "User", back_populates="addresses"
    )