from uuid import UUID
from fastapi import HTTPException,status
from app.models.conversation import Conversation
from app.repositories.conversation import ConversationRepositoty
from app.schemas.conversation import ConversationCreate

class ConversationService:
    def __init__(
        self,
        repository: ConversationRepositoty,
    ):
        self.repository = repository

    async def create(
        self,
        user_id: UUID,
        data: ConversationCreate,
    ) -> Conversation:

        conversation = Conversation(
            user_id=user_id,
            title=data.title,
        )

        return await self.repository.create(
            conversation
        )

    async def get_owned_conversation(
        self,
        conversation_id: UUID,
        user_id: UUID,
    ) -> Conversation:

        conversation = await self.repository.get_by_id(
            conversation_id
        )

        if conversation is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found",
            )

        if conversation.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found",
            )

        return conversation

    async def list_user_conversations(
        self,
        user_id: UUID,
    ) -> list[Conversation]:

        return await self.repository.get_by_user(
            user_id
        )

    async def delete(
        self,
        conversation_id: UUID,
        user_id: UUID,
    ) -> None:

        conversation = await self.get_owned_conversation(
            conversation_id,
            user_id,
        )

        await self.repository.delete(conversation)