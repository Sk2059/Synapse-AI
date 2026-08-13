from uuid import UUID

from fastapi import HTTPException,status

from app.models.message import Message,MessageRole
from app.schemas.message import MessageCreate
from app.repositories.message import MessageRepositoty
from app.repositories.conversation import ConversationRepositoty

class MessageService:
    def __init__(
            self,
            message_repository : MessageRepositoty,
            conversation_repository : ConversationRepositoty
    ):
        self.message_repository = message_repository
        self.conversation_repository = conversation_repository

    async def create_user_message(
            self,
            conversation_id:UUID,
            user_id : UUID,
            data:MessageCreate
    ) -> Message:
        conversation = await self.conversation_repository.get_by_id(
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

        message = Message(
            conversation_id=conversation_id,
            role = MessageRole.USER,
            content = data.content
        )

        return await self.message_repository.create(
            message
        )
    
