from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base

class MediaAsset(Base):
    __tablename__ = "media_assets"

    id = Column(Integer, primary_key=True, index=True)
    original_filename = Column(String(255), nullable=False)
    stored_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_url = Column(String(500), nullable=False)
    content_type = Column(String(100), nullable=False)
    file_size = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)

    proofs = relationship(
            "Proof",
            back_populates="media_asset"
        )
    
class Proof(Base):
    __tablename__ = "proofs"

    id = Column(Integer, primary_key=True, index=True)
    daily_routine_item_id = Column(
        Integer,
        ForeignKey("daily_routine_items.id"),
        nullable=False,
        index=True,
    )
    media_asset_id = Column(
        Integer,
        ForeignKey("media_assets.id"),
        nullable=False,
        index=True,
    )
    note = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)

    daily_routine_item = relationship(
        "DailyRoutineItem",
        back_populates="proofs"
    )
    media_asset = relationship(
        "MediaAsset",
        back_populates="proofs"
    )
