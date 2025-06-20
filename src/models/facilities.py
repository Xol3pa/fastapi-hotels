from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey, Index, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if TYPE_CHECKING:
    from src.models import RoomsModel


class FacilitiesModel(Base):
    __tablename__ = "facilities"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))

    __table_args__ = (
        Index("ix_facilities_title_lower", func.lower(title), unique=True),
    )

    rooms: Mapped[list["RoomsModel"]] = relationship(
        secondary="rooms_facilities", back_populates="facilities"
    )


class RoomsFacilitiesModel(Base):
    __tablename__ = "rooms_facilities"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    facility_id: Mapped[int] = mapped_column(ForeignKey("facilities.id"))
