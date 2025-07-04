from sqlalchemy.ext.asyncio import AsyncSession


class GetChatIdService:

    @staticmethod
    async def get_chat_id(session: AsyncSession, chat_url: str):
        ...
