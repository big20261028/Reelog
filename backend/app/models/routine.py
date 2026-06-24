from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base

class Routine(Base):
    __tablename__ = "routines"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)

    items = relationship(
        "RoutineItem",
        back_populates="routine",
        cascade="all, delete-orphan",
    )

class RoutineItem(Base):
    __tablename__ = "routine_items"

    id = Column(Integer, primary_key=True, index=True)
    routine_id = Column(
        Integer,
        ForeignKey("routines.id"),
        nullable=False,
        index=True
    )
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    sequence = Column(Integer, nullable=False, default=1)

    routine = relationship(
        "Routine",
        back_populates="items"
    )