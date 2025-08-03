from fastapi import Request

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.schemas.scenario_schema import ScenarioCreate

from src.metadata.scenario_metadata import ACTIONS_METADATA, CONDITIONS_METADATA
from src.dependency import scenario_service

router = APIRouter(prefix="/scenarios")

"""get scenario metadata"""


@router.get("/metadata/actions")
async def get_actions_metadata():
    return ACTIONS_METADATA


@router.get("/metadata/conditions")
async def get_conditions_metadata():
    return CONDITIONS_METADATA


"""Call this router in api_gateway"""


@router.post("/create")
async def create_scenario(
        request: Request,
        data: ScenarioCreate,
        session: AsyncSession = Depends(get_session)
):
    return await scenario_service.create_scenario(session, data, request)
