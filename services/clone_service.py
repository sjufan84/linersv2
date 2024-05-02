import numpy as np
import base64
from scipy.io.wavfile import write
from io import BytesIO
from fastapi import UploadFile
import logging
from infer.lib.audio import load_audio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def clone_liner_vocals(audio_file: UploadFile, artist: str = "Joel", f0_adjustment: int = 0):
    """
    Clones the vocals from an audio file.
y
    Args:
    audio_file (UploadFile): The audio file to clone vocals from.

    Returns:
    str: A Base64 string of the cloned vocals audio file.
    """
    logger.info(f"""Cloning vocals from {audio_file.filename} with artist {artist}
    and f0_adjustment {f0_adjustment}""")
    audio_bytes = await audio_file.read()
    audio = load_audio(audio_bytes, 48000)

    # Convert numpy array to a list of floats
    audio = audio.tolist()

    return audio[:100]
    
    '''logger.info(f"{vocals[1]}")
    audio_array = vocals[1][1]
    sr = vocals[1][0]

    # Convert numpy array to byte stream
    byte_stream = BytesIO()
    write(byte_stream, sr, np.array(audio_array, dtype=np.int16))

    # Convert byte stream to Base64 string
    base64_audio = base64.b64encode(byte_stream.getvalue()).decode('utf-8')
    logger.info(f"Vocals cloned successfully. Returning Base64 string {base64_audio[:50]}")

    return base64_audio'''
