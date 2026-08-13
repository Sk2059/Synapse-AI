from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.repositories.conversation import ConversationRepository
from app.repositories.message import MessageRepository
from app.schemas.message import (
    MessageCreate,
    MessageResponse,
)
from app.services.message import MessageService


router = APIRouter(
    prefix="/conversations",
    tags=["Messages"],
)

@router.post(
    "/{conversation_id}/messages",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_message(
    conversation_id: UUID,
    data: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    message_repository = MessageRepository(db)
    conversation_repository = ConversationRepository(db)

    service = MessageService(
        message_repository=message_repository,
        conversation_repository=conversation_repository,
    )

    return await service.create_user_message(
        conversation_id=conversation_id,
        user_id=current_user.id,
        data=data,
    )

@router.get(
    "/{conversation_id}/messages",
    response_model=list[MessageResponse],
)
async def list_messages(
    conversation_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    conversation_repository = ConversationRepository(db)
    conversation = await conversation_repository.get_by_id(
        conversation_id
    )

    if (
        conversation is None
        or conversation.user_id != current_user.id
    ):
        from fastapi import HTTPException

        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    message_repository = MessageRepository(db)

    return await message_repository.get_by_conversation(
        conversation_id
    )