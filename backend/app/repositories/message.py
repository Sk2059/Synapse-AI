from uuid import UUID
from sqlalchemy import select 
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.message import Message

class MessageRepositoty():
    def __init__(self, session : AsyncSession):
        self.session = session

    async def create(self, message:Message) -> Message:
        self.session.add(message)
        self.session.commit()
        self.session.refresh(message)

        return message

    async def get_by_id(
            self,
            message_id:UUID
    ) -> Message | None:
        result = await self.session.execute(
            select(Message).where(
                Message.id == message_id
            )
        )
        return result.scalar_one_or_none()

    async def get_by_conversation(
            self,
            conversation_id : UUID,
    )-> list[Message]:
        result = await self.session.execute(
            select(Message)
            .where(
                Message.conversation_id == conversation_id
            )
            .order_by(
                Message.created_at.asc()
            )
        )

        return list(result.scalars().all())
