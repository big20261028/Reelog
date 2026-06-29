from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base

class DailyRoutine(Base):
    __tablename__ = "daily_routines"
    
    __table_args__ = (
        UniqueConstraint(
            "routine_id", "target_date", name="uq_daily_routine_routine_date",
        ),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    
    routine_id = Column(
        Integer,
        ForeignKey("routines.id"),
        nullable=False,
        index=True
    )
    
    target_date = Column(Date, nullable=False, index=True)
    
    title = Column(String(100), nullable=False) # 새로 선언 하는 이유
    description = Column(Text, nullable=True) # 종속성 제거해서 템플릿 루틴이 변경될 경우에도 값을 유지하기 위해
    status = Column(String(20), nullable=False, default="PENDING")
    
    items = relationship(
        "DailyRoutineItem",
        back_populates="daily_routine",
        cascade="all, delete-orphan",
    )
    
class DailyRoutineItem(Base):
    __tablename__ = "daily_routine_items"

    id = Column(Integer, primary_key=True, index=True)
    
    daily_routine_id = Column(
        Integer,
        ForeignKey("daily_routines.id"),
        nullable=False,
        index=True,
    )
    
    routine_item_id = Column(
        Integer,
        ForeignKey("routine_items.id"),
        nullable=False,
        index=True
    )
    
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    sequence = Column(Integer, nullable=False, default=1)
    
    is_completed = Column(Boolean, nullable=False, default=False)
    completed_at = Column(DateTime, nullable=True)
    
    daily_routine = relationship(
        "DailyRoutine",
        back_populates="items"
    )

    proofs = relationship(
        "Proof",
        back_populates="daily_routine_item",
        cascade="all, delete-orphan"
    )

    @property
    def proof_count(self):
        return len(self.proofs)