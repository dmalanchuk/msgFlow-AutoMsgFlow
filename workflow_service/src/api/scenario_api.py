from fastapi import Request

from fastapi import APIRouter, Depends
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.schemas.scenario_schema import ScenarioCreate
from src.schemas.scenario_update_schema import UpdateScenario, UpdateEvent

from src.metadata.scenario_metadata import ACTIONS_METADATA, CONDITIONS_METADATA
from src.utils.get_user_email import get_user_email

from src.services.scenario_service import (
    create_scenario_service, delete_scenario_service,
    get_scenarios_service
)

from src.services.scenario_update_service import update_scenario_service, update_eca_service

router = APIRouter(prefix="/scenarios")


@router.get("/actions/metadata")
async def get_actions_metadata():
    return ACTIONS_METADATA


@router.get("/conditions/metadata")
async def get_conditions_metadata():
    return CONDITIONS_METADATA


@router.post(
    "/scenario",
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
    return await create_scenario_service(session, data, request)


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
        owner_email: EmailStr = Depends(get_user_email),
        session: AsyncSession = Depends(get_session)
):
    return await delete_scenario_service(name, owner_email, session)


@router.patch(
    "/{name}",
    summary="Update scenario by name",
    description="With this endpoint you can update some params by the name of your script",
    status_code=200,
    responses={
        200: {"description": "Scenario updated successfully"},
        404: {"description": "Scenario not found"}
    },
)
async def update_param_by_name(
        name: str,
        body: UpdateScenario,
        owner_email: EmailStr = Depends(get_user_email),
        session: AsyncSession = Depends(get_session)
):
    return await update_scenario_service(name, owner_email, body, session)


@router.patch(
    "/{name}/event",
    summary="Update scenario by name",
    description="With this endpoint you can update some params by the name of your script",
    status_code=200,
    responses={
        200: {"description": "Scenario updated successfully"},
        404: {"description": "Scenario not found"}
    },
)
async def update_event(
        name: str,
        body: UpdateEvent,
        owner_email: EmailStr = Depends(get_user_email),
        session: AsyncSession = Depends(get_session)
):
    return await update_eca_service(name, owner_email, body, session)


@router.get(
    "/list",
    summary="Get all scenarios",
    description="endpoint for getting all scenarios",
    status_code=200,
    responses={
        404: {"description": "Scenario not found"}
    },
)
async def get_scenarios(
        email: EmailStr = Depends(get_user_email),
        session: AsyncSession = Depends(get_session)
):
    return await get_scenarios_service(email, session)
