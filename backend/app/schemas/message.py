from enum import Enum
from uuid import UUID
from datetime import datetime 
from pydantic import BaseModel, Field,ConfigDict
from app.models.message import MessageRole


class MessageCreate(BaseModel):
    content: str = Field(
        min_length=1,
        max_length=100_000,
    )

class MessageResponse(BaseModel):
    id: UUID
    conversation_id: UUID
    role: MessageRole
    content: str
    token_input: int | None
    token_output: int | None
    cost: float | None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )