 # infrastructure/db/models.py
from datetime import datetime
from decimal import Decimal
from typing import Optional
from sqlalchemy import ForeignKey, String, Numeric, Table, Column, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from base import Base

# Table d'association many-to-many simple
product_category = Table(
    "product_category", Base.metadata,
    Column("product_id", ForeignKey("products.id", ondelete="CASCADE"), primary_key=True),
    Column("category_id", ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True),
)

class UserModel(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # one-to-one
    profile: Mapped[Optional["ProfileModel"]] = relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan")
    # one-to-many
    orders: Mapped[list["OrderModel"]] = relationship(back_populates="user")

class ProfileModel(Base):
    __tablename__ = "profiles"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True)  # unique => 1-1
    phone: Mapped[Optional[str]] = mapped_column(String(30))
    user: Mapped["UserModel"] = relationship(back_populates="profile")

class OrderModel(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    status: Mapped[str] = mapped_column(String(20), default="PENDING")
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    user: Mapped["UserModel"] = relationship(back_populates="orders")      # many-to-one
    items: Mapped[list["OrderItemModel"]] = relationship(
        back_populates="order", cascade="all, delete-orphan")

class ProductModel(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    # many-to-many simple
    categories: Mapped[list["CategoryModel"]] = relationship(
        secondary=product_category, back_populates="products")

class CategoryModel(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id"))

    products: Mapped[list["ProductModel"]] = relationship(
        secondary=product_category, back_populates="categories")
    # auto-référence (arbre)
    parent: Mapped[Optional["CategoryModel"]] = relationship(
        remote_side="CategoryModel.id", back_populates="children")
    children: Mapped[list["CategoryModel"]] = relationship(back_populates="parent")

# many-to-many AVEC données supplémentaires => "association object"
class OrderItemModel(Base):
    __tablename__ = "order_items"
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), primary_key=True)
    quantity: Mapped[int]
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))  # prix figé à l'achat

    order: Mapped["OrderModel"] = relationship(back_populates="items")
    product: Mapped["ProductModel"] = relationship()