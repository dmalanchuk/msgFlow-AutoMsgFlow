from fastapi import APIRouter
from src.metadata.scenario_metadata import ACTIONS_METADATA, CONDITIONS_METADATA

router = APIRouter()


@router.get("/metadata/actions")
async def get_actions_metadata():
    return ACTIONS_METADATA


@router.get("/metadata/conditions")
async def get_conditions_metadata():
    return CONDITIONS_METADATA
