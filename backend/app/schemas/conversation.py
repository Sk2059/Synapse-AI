from pydantic import BaseModel , Field, ConfigDict
from datetime import datetime
from uuid import UUID

class ConversationCreate(BaseModel):
    title : str = Field(
        default="new chat",
        max_length=255,
    )

class ConversationResponse(BaseModel):
    id: UUID
    title: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
    
