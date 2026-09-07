from app.database.connection import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    String, 
    Text, 
    Enum as SQLAEnum, 
    Integer, 
    Boolean, 
    DateTime, 
    func, 
    ForeignKey,
    Float
)
from enum import Enum
from datetime import datetime

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.categories.models import Category, SubCategory
    from app.users.models import User


class TargetKey(str, Enum):
    UOMO = "uomo"
    DONNA = "donna"
    BAMBINO = "bambino"
    BAMBINA = "bambina"


class Product(Base):

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    title: Mapped[str] = mapped_column(String(100), nullable=False)
    subtitle: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    # genera sequenza per url
    slug: Mapped[str] = mapped_column(
        String(100), 
        nullable=False, 
        unique=True, 
        index=True
    )

    price_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    sale_percent: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )
    new_arrivals: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        index=True
    )
    image_url: Mapped[str] = mapped_column(
        String(300),
        nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        index=True
    )
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
    
    # relationship with subcategory model [ONE TO MANY]
    sub_category_id: Mapped[int] = mapped_column(
        ForeignKey("sub_categories.id", ondelete="CASCADE"), nullable=False
    )
    sub_category: Mapped["SubCategory"] = relationship(
        "SubCategory", 
        back_populates="products",
        passive_deletes=True,
    )

    # relationship with product variants model [ONE TO MANY]
    variants: Mapped[list["ProductVariant"]] = relationship(
        "ProductVariant", 
        back_populates="product", 
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    # relationship with product reviews model [ONE TO MANY]
    reviews: Mapped[list["ProductReviews"]] = relationship(
        "ProductReviews", 
        back_populates="product", 
        cascade="all, delete-orphan",
        passive_deletes=True
    )

class ProductVariant(Base):

    __tablename__ = "product_variants"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    size: Mapped[str] = mapped_column(String(20), nullable=False)
    
    color_name: Mapped[str] = mapped_column(String(100), nullable=False)
    color_hex: Mapped[str] = mapped_column(String(7), nullable=False)

    target_key: Mapped[TargetKey] = mapped_column(
        SQLAEnum(TargetKey),
        nullable=False
    )

    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # relationship with product model [MANY TO ONE]
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    product: Mapped[Product] = relationship(
        "Product", back_populates="variants"
    )


class ProductReviews(Base):
    __tablename__  = "product_reviews"
    
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
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    user: Mapped[User] = relationship(
        "User", 
        back_populates="product_reviews",
    )
    
    # relationship with product model [MANY TO ONE]
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"), 
        nullable=False
    )
    product: Mapped[Product] = relationship(
        "Product", back_populates="reviews"
    )
    