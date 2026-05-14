from datetime import date, datetime
from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    owner_name: Mapped[str] = mapped_column(String(100), nullable=False)
    account_number: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)
    balance: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="RUB", nullable=False)
    account_type: Mapped[str] = mapped_column(String(20), default="checking", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    outgoing_transfers: Mapped[list["Transfer"]] = relationship(
        "Transfer", foreign_keys="Transfer.from_account_id", back_populates="from_account"
    )
    incoming_transfers: Mapped[list["Transfer"]] = relationship(
        "Transfer", foreign_keys="Transfer.to_account_id", back_populates="to_account"
    )
    cards: Mapped[list["Card"]] = relationship("Card", back_populates="account", cascade="all, delete-orphan")


class Transfer(Base):
    __tablename__ = "transfers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    from_account_id: Mapped[int] = mapped_column(Integer, ForeignKey("accounts.id"), nullable=False, index=True)
    to_account_id: Mapped[int] = mapped_column(Integer, ForeignKey("accounts.id"), nullable=False, index=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="RUB", nullable=False)
    fee: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False, index=True)

    from_account: Mapped["Account"] = relationship("Account", foreign_keys=[from_account_id], back_populates="outgoing_transfers")
    to_account: Mapped["Account"] = relationship("Account", foreign_keys=[to_account_id], back_populates="incoming_transfers")


class Card(Base):
    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    account_id: Mapped[int] = mapped_column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    card_number: Mapped[str] = mapped_column(String(16), unique=True, index=True, nullable=False)
    holder_name: Mapped[str] = mapped_column(String(100), nullable=False)
    expires_at: Mapped[date] = mapped_column(Date, nullable=False)
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    account: Mapped["Account"] = relationship("Account", back_populates="cards")
