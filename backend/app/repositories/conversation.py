from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.conversation import Conversation

class ConversationRepositoty:

    def __init__(self, session=AsyncSession):
        self.session = session

    async def create(
            self,
            conversation=Conversation
    ):
        self.session.add(conversation)

        await self.session.commit()
        await self.session.refresh(conversation)

        return conversation

    async def get_by_id(
            self,
            conversation_id:UUID
    ) -> Conversation | None :
        result = await self.session.execute(
            select(Conversation).where(
                Conversation.id == conversation_id
            )
        )
        return result.scalar_one_or_none()

    async def get_by_user(
            self,
            user_id = UUID
    ) -> list[Conversation]:
        result = await self.session.execute(
            select(Conversation)
            .where(
                Conversation.user_id == user_id
            )
            .order_by(
                Conversation.updated_at.desc()
            )
        )

        return list(result.scalars().all())

    async def delete(
            self,
            conversation: Conversation
    ) -> None:
        await self.session.delete(conversation)

        await self.session.commit()
        
        
