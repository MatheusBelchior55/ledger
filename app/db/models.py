from datetime import datetime
from typing import List, Optional
import enum
from decimal import Decimal
from sqlalchemy import Numeric

from sqlalchemy import Enum, ForeignKey, Integer, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class TransactionType(enum.Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"


class Base(DeclarativeBase):
    pass


class Organization(Base):
    __tablename__ = "organization"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str]
    email: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())

    users: Mapped[List["User"]] = relationship(
        back_populates="organization"
    )

    accounts: Mapped[List["Account"]] = relationship(
        back_populates="organization"
    )

    categories: Mapped[List["Category"]] = relationship(
        back_populates="organization"
    )


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str]
    email: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(insert_default=func.now())

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organization.id")
    )

    organization: Mapped["Organization"] = relationship(
        back_populates="users"
    )


class Account(Base):
    __tablename__ = "account"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str]
    balance: Mapped[Decimal] = mapped_column(Numeric(15, 2))
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organization.id")
    )

    organization: Mapped["Organization"] = relationship(
        back_populates="accounts"
    )

    transactions: Mapped[List["Transaction"]] = relationship(
        back_populates="account"
    )


class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organization.id")
    )

    organization: Mapped["Organization"] = relationship(
        back_populates="categories"
    )

    transactions: Mapped[List["Transaction"]] = relationship(
        back_populates="category"
    )


class Transaction(Base):
    __tablename__ = "transaction"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    value: Mapped[Decimal] = mapped_column(Numeric(15, 2))

    type: Mapped[TransactionType] = mapped_column(
        Enum(TransactionType, name="transaction_type_enum")
    )

    account_id: Mapped[int] = mapped_column(
        ForeignKey("account.id")
    )

    category_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("category.id")
    )

    account: Mapped["Account"] = relationship(
        back_populates="transactions"
    )

    category: Mapped[Optional["Category"]] = relationship(
        back_populates="transactions"
    )