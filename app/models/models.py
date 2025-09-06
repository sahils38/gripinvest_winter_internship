from __future__ import annotations

from datetime import datetime, date
from decimal import Decimal
from typing import Optional
import enum

from sqlalchemy import (
    String, Integer, DateTime, DECIMAL, Enum, ForeignKey, Text, func
)
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

# --- Enums from the spec ---
class RiskAppetite(str, enum.Enum):
    low = "low"; moderate = "moderate"; high = "high"

class InvType(str, enum.Enum):
    bond = "bond"; fd = "fd"; mf = "mf"; etf = "etf"; other = "other"

class RiskLevel(str, enum.Enum):
    low = "low"; moderate = "moderate"; high = "high"

class InvStatus(str, enum.Enum):
    active = "active"; matured = "matured"; cancelled = "cancelled"


# --- users table ---
class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[Optional[str]] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    risk_appetite: Mapped[RiskAppetite] = mapped_column(
        Enum(RiskAppetite), default=RiskAppetite.moderate, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.current_timestamp()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp()
    )


# --- investment_products table ---
class InvestmentProduct(Base):
    __tablename__ = "investment_products"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    investment_type: Mapped[InvType] = mapped_column(Enum(InvType), nullable=False)
    tenure_months: Mapped[int] = mapped_column(Integer, nullable=False)
    annual_yield: Mapped[Decimal] = mapped_column(DECIMAL(5, 2), nullable=False)
    risk_level: Mapped[RiskLevel] = mapped_column(Enum(RiskLevel), nullable=False)
    min_investment: Mapped[Decimal] = mapped_column(DECIMAL(12, 2), server_default="1000.00")
    max_investment: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(12, 2))
    description: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.current_timestamp()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp()
    )


# --- investments table ---
class Investment(Base):
    __tablename__ = "investments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    product_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("investment_products.id", ondelete="CASCADE"), nullable=False
    )
    amount: Mapped[Decimal] = mapped_column(DECIMAL(12, 2), nullable=False)
    invested_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.current_timestamp()
    )
    status: Mapped[InvStatus] = mapped_column(
        Enum(InvStatus), server_default=InvStatus.active.value, nullable=False
    )
    expected_return: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(12, 2))
    maturity_date: Mapped[Optional[date]]


# --- transaction_logs table ---
class TransactionLog(Base):
    __tablename__ = "transaction_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id"))
    email: Mapped[Optional[str]] = mapped_column(String(255))
    endpoint: Mapped[str] = mapped_column(String(255), nullable=False)
    http_method: Mapped[str] = mapped_column(
        Enum("GET", "POST", "PUT", "DELETE", name="http_method_enum"), nullable=False
    )
    status_code: Mapped[int] = mapped_column(Integer, nullable=False)
    error_message: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.current_timestamp()
    )
