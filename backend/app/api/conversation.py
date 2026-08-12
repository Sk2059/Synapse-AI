from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.repositories.conversation import ConversationRepositoty
from app.schemas.conversation import (
    ConversationCreate,
    ConversationResponse,
)
from app.services.conversation import ConversationService


router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)

@router.post(
    "",
    response_model=ConversationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_conversation(
    data: ConversationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repository = ConversationRepositoty(db)

    service = ConversationService(repository)

    return await service.create(
        user_id=current_user.id,
        data=data,

    )

@router.get(
    "",
    response_model=list[ConversationResponse],
)
async def list_conversations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repository = ConversationRepositoty(db)

    service = ConversationService(repository)

    return await service.list_user_conversations(
        current_user.id
    )

@router.get(
    "/{conversation_id}",
    response_model=ConversationResponse,
)
async def get_conversation(
    conversation_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repository = ConversationRepositoty(db)

    service = ConversationService(repository)

    return await service.get_owned_conversation(
        conversation_id=conversation_id,
        user_id=current_user.id,
    )

@router.delete(
    "/{conversation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_conversation(
    conversation_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repository = ConversationRepositoty(db)

    service = ConversationService(repository)

    await service.delete(
        conversation_id=conversation_id,
        user_id=current_user.id,
    )