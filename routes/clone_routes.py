# FastAPI endpoints for the LinerGenV1 project.
from fastapi import APIRouter, UploadFile, File, Form
from typing import Optional
from services.clone_service import clone_liner_vocals
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

'''class CloneVocalsRequest(BaseModel):
    audio_file: UploadFile = Field(File(...), description="The audio file to clone vocals from.")
    artist: str = Field(None, description="The artist of the song.")'''

@router.post("/clone_vocals")
async def clone_vocals_endpoint(
    audio_file: UploadFile = File(...), artist: Optional[str] = Form(None),
    f0_adjustment: Optional[str] = Form(None)
):

    """
    Clones the vocals from an audio file.

    Args:
    audio_file (UploadFile): The audio file to clone vocals from.
    artist (str): The artist of the song.


    Returns:
    str: A Base64 string of the cloned vocals audio file.
    """
    f0_adjustment = int(f0_adjustment) if f0_adjustment is not None else None
    logger.info(f"Cloning vocals from audio file: {audio_file.filename}")
    logger.info(f"Artist: {artist}")
    logger.info(f"f0_adjustment: {f0_adjustment}")

    cloned_vocals = await clone_liner_vocals(audio_file, artist=artist, f0_adjustment=f0_adjustment)

    logger.info(f"Cloned vocals audio: {cloned_vocals[:100]}")

    return {"cloned_vocals": cloned_vocals}
