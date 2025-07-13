from src.models.scenarios_model import ScenariosModel
from src.schemas.event_schema import Event

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_


class EventRepo:

    @staticmethod
    async def get_event(data: Event, session: AsyncSession):
        scenario = await session.execute(
            select(ScenariosModel).where(
                and_(
                    ScenariosModel.chat_id == data.chat_id,
                    ScenariosModel.event['source'].astext == data.source,
                    ScenariosModel.event['type'].astext == data.event_type
                )
            )
        )

        return scenario.scalars().all()
