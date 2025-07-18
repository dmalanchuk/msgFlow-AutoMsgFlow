from fastapi import Request, Body
from src.database import get_session

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from src.database import get_session
from src.services.scenario_get_email_service import ScenarioGetEmailService
from src.services.scenario_service import ScenarioService
from src.schemas.scenario_schema import ScenarioCreate

from src.metadata.scenario_metadata import ACTIONS_METADATA, CONDITIONS_METADATA

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
    return await ScenarioService.create_scenario(session, data, request)
