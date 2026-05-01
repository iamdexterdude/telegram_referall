"""
bot/database/models.py — ORM models (SQLite now, PostgreSQL-ready).
"""
from datetime import datetime

from sqlalchemy import (
    BigInteger, Boolean, DateTime, ForeignKey,
    Integer, String, UniqueConstraint, func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True)
    username: Mapped[str | None] = mapped_column(String(64), nullable=True)
    first_name: Mapped[str] = mapped_column(String(128), nullable=False)
    last_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    phone_number: Mapped[str | None] = mapped_column(String(32), nullable=True)
    referral_code: Mapped[str] = mapped_column(String(16), unique=True, nullable=False, index=True)
    referral_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    referred_by: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    language: Mapped[str] = mapped_column(String(4), nullable=False, default="en")
    is_banned: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    link_clicks: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    referrals_made: Mapped[list["Referral"]] = relationship(
        "Referral", foreign_keys="[Referral.referrer_id]", back_populates="referrer"
    )

    def full_name(self) -> str:
        parts = [self.first_name]
        if self.last_name:
            parts.append(self.last_name)
        return " ".join(parts)

    def display_name(self) -> str:
        if self.username:
            return f"@{self.username}"
        return self.full_name()


class Referral(Base):
    __tablename__ = "referrals"
    __table_args__ = (
        UniqueConstraint("referred_user_id", name="uq_referral_referred_user"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    referrer_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.user_id"), nullable=False, index=True
    )
    referred_user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.user_id"), nullable=False, unique=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    referrer: Mapped["User"] = relationship(
        "User", foreign_keys=[referrer_id], back_populates="referrals_made"
    )
