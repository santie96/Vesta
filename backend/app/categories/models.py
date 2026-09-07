from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, ForeignKey
from app.database.connection import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.products.models import Product

class Category(Base):

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    # relationship with sub_category model [ONE TO MANY]
    sub_categories: Mapped[list["SubCategory"]] = relationship(
        "SubCategory", 
        back_populates="category", 
        cascade="all, delete-orphan",
        passive_deletes=True
    )


class SubCategory(Base):

    __tablename__ = "sub_categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    # relationship with category model [MANY TO ONE]
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"), nullable=False
    )
    category: Mapped["Category"] = relationship(
        "Category", 
        back_populates="sub_categories",
    )

    # relationship with product model [ONE TO MANY]
    products: Mapped[list["Product"]] = relationship(
        "Product", 
        back_populates="sub_category", 
        cascade="all, delete-orphan",
        passive_deletes=True
    )

