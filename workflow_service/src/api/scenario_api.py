from fastapi import Request, Body

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.schemas.scenario_schema import ScenarioCreate, ScenarioPatchUpdate

from src.metadata.scenario_metadata import ACTIONS_METADATA, CONDITIONS_METADATA
from src.dependency import scenario_service

router = APIRouter(prefix="/scenarios")


@router.get("/actions/metadata")
async def get_actions_metadata():
    return ACTIONS_METADATA


@router.get("/conditions/metadata")
async def get_conditions_metadata():
    return CONDITIONS_METADATA


@router.post(
    "",
    summary="Create new scenario",
    description="This endpoint allows you to create a new script by template",
    status_code=201,
    responses={
        201: {"description": "Scenario created successfully"},
        400: {"description": "Invalid request"},
    },
)
async def create_scenario(
        request: Request,
        data: ScenarioCreate,
        session: AsyncSession = Depends(get_session)
):
    return await scenario_service.create_scenario(session, data, request)


@router.delete(
    "/{name}",
    summary="Delete scenario by name",
    description="This endpoint allows you to delete a scenario by name",
    status_code=204,
    responses={
        404: {"description": "Scenario not found"}
    },
)
async def delete_scenario_by_name(
        name: str,
        session: AsyncSession = Depends(get_session)
):
    return await scenario_service.delete_scenario(name, session)


@router.patch(
    "/{id}",
    summary="Update scenario by name",
    description="With this endpoint you can update some params by the name of your script",
    status_code=200,
    responses={
        200: {"description": "Scenario updated successfully"},
        404: {"description": "Scenario not found"}
    },
)
async def update_param_by_id(
        id: int,
        body: ScenarioPatchUpdate = Body(...),
        session: AsyncSession = Depends(get_session)
):
    return await scenario_service.update_scenario_patch(id, session, body)


@router.get(
    "",
    summary="Get all scenarios",
    description="endpoint for getting all scenarios",
    status_code=200,
    responses={
        404: {"description": "Scenario not found"}
    },
)
async def get_scenarios(
        chat_id: int,
        session: AsyncSession = Depends(get_session)
):
    # To-Do: Make to the current mail so that the user can only see their scripts
    return await scenario_service.get_scenarios(chat_id, session)
