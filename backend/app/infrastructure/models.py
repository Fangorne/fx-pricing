"""SQLAlchemy 2.0 ORM models for FX reference data."""

from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class FxConventionModel(Base):
    __tablename__ = "fx_conventions"

    pair: Mapped[str] = mapped_column(String(7), primary_key=True)
    spot_lag: Mapped[int] = mapped_column(Integer, nullable=False)
    day_count: Mapped[str] = mapped_column(String(20), nullable=False)
    roll_convention: Mapped[str] = mapped_column(String(30), nullable=False)
    pip_precision: Mapped[int] = mapped_column(Integer, nullable=False)
    quotation_side: Mapped[str] = mapped_column(String(10), nullable=False)


class MarketCalendarModel(Base):
    __tablename__ = "market_calendars"

    currency: Mapped[str] = mapped_column(String(3), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    holidays: Mapped[list["HolidayModel"]] = relationship(
        back_populates="calendar", cascade="all, delete-orphan"
    )


class HolidayModel(Base):
    __tablename__ = "holidays"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    currency: Mapped[str] = mapped_column(
        String(3), ForeignKey("market_calendars.currency"), nullable=False, index=True
    )
    holiday_date: Mapped[date] = mapped_column(Date, nullable=False)
    description: Mapped[str] = mapped_column(String(100), nullable=False, default="")

    calendar: Mapped["MarketCalendarModel"] = relationship(back_populates="holidays")
