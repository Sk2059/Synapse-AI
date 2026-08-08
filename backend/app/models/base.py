from datetime import datetime
from uuid import uuid4, UUID

from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import DeclarativeBase , Mapped, mapped_column

class Base(DeclarativeBase):
    """Base for all orm models"""
    pass

class TimestampMixin:
    created_at:Mapped[datetime]= mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

class UUIDMixin:
    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        unique=True,
        nullable=False,
    )

class BaseModel(Base, TimestampMixin, UUIDMixin):
    """Base model for all orm models"""
    __abstract__ = True

