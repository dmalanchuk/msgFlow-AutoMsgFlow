from src.models.scenarios_model import ScenariosModel
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select, and_


class EventRepo:

    @staticmethod
    async def get_event(chat_id: int, source: str, event_type: str, session: AsyncSession):
        scenario = await session.execute(
            select(ScenariosModel).where(
                and_(
                    ScenariosModel.chat_id == chat_id,
                    ScenariosModel.event['source'].astext == source,
                    ScenariosModel.event['type'].astext == event_type
                )
            )
        )

        return scenario.scalars().all()
