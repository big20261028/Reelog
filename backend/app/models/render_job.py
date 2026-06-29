from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base

class RenderJob(Base):
    __tablename__ = "render_jobs"

    id = Column(Integer, primary_key=True, index=True)
    daily_routine_id = Column(
        Integer,
        ForeignKey("daily_routines.id"),
        nullable=False,
        index=True
    )
    
    status = Column(String(20), nullable=False, default="PENDING")

    # 생성한 영상과 관계를 맺는 필드?
    output_media_asset_id = Column(
        Integer,
        ForeignKey("media_assets.id"),
        nullable=True, # 생성되지 않았을 수 있으므로 True인가?
        index=True
    )

    error_message = Column(Text, nullable=True)

    created_at = Column(DateTime, nullable=False, default=datetime.now)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    daily_routine = relationship("DailyRoutine")
    output_media_asset = relationship("MediaAsset")

    items = relationship(
        "RenderJobItem",
        back_populates="render_job",
        cascade="all, delete-orphan",
    )
    
class RenderJobItem(Base):
    __tablename__ = "render_job_items"

    __table_args__ = (
        UniqueConstraint(
            "render_job_id",
            "daily_routine_item_id",
            name="uq_render_job_item_daily_routine_item",
        ),
        UniqueConstraint(
            "render_job_id",
            "sequence",
            name="uq_render_job_item_sequence",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    render_job_id = Column(
        Integer,
        ForeignKey("render_jobs.id"),
        nullable=False,
        index=True,
    )

    daily_routine_item_id = Column(
        Integer,
        ForeignKey("daily_routine_items.id"),
        nullable=False,
        index=True,
    )

    proof_id = Column(
        Integer,
        ForeignKey("proofs.id"),
        nullable=False,
        index=True
    )

    sequence = Column(Integer, nullable=False, default=1)

    render_job = relationship(
        "RenderJob",
        back_populates="items"# 양방향 관계일때만 쓰는 매개변수인가?
    )
    daily_routine_item = relationship("DailyRoutineItem")
    proof = relationship("Proof")