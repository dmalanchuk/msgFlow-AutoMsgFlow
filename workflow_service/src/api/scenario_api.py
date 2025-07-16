from fastapi import Request
from src.database import get_session

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from src.database import get_session
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


"""Create scenario"""


@router.post("/create")
async def create_scenario(
        data: Annotated[ScenarioCreate, Depends()],
        session: AsyncSession = Depends(get_session)
):
    return await ScenarioService.create_scenario(session, data)

@router.post("/scenarios")
async def create_scenario(
        request: Request,
        scenario_data: ScenarioCreate,
        session: AsyncSession = Depends(get_session)
):
    # Отримуємо email з request.state
    user_email = request.state.user_email if hasattr(request.state, "user_email") else request.headers.get("x-user-email")

    if not user_email:
        raise HTTPException(status_code=401, detail="User email not found")

    return await ScenarioService.create_scenario(session, scenario_data, owner_email=user_email)
