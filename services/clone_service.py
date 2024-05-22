from configs.config import Config
from infer.modules.vc.modules import VC
import logging
import numpy as np
import base64
from scipy.io.wavfile import write
from io import BytesIO

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def save_audio_to_wav(numpy_audio_array, filename, sample_rate):
    write(filename, sample_rate, numpy_audio_array)


async def get_clone_vocals(
    device,
    is_half,
    model_name,
    input_path,
    f0up_key,
    f0method,
    index_path,
    index_rate,
    filter_radius,
    resample_sr,
    rms_mix_rate,
    protect,
    opt_path,
):
    config = Config()
    config.device = device if device else config.device
    config.is_half = is_half if is_half else config.is_half
    vc = VC(config)
    vc.get_vc(model_name)
    _, wav_opt = vc.vc_single(
        0,
        input_path,
        f0up_key,
        None,
        f0method,
        index_path,
        None,
        index_rate,
        filter_radius,
        resample_sr,
        rms_mix_rate,
        protect,
    )
    # Output the file to a mp3 file

    return (wav_opt[0], wav_opt[1])


async def clone_liner_vocals(
    input_audio: str, artist="Joel Kaiser", f0_adjustment: int = 0
):
    model_name = "brent2.pth"
    input_path = input_audio
    f0up_key = 0
    f0method = "rmvpe"
    index_path = "logs/added_IVF3962_Flat_nprobe_1_brent2_v2.index"
    index_rate = 0.75
    filter_radius = 3
    resample_sr = 48000
    rms_mix_rate = 0.25
    protect = 0.33
    opt_path = "output.wav"
    sr, audio = await get_clone_vocals(
        None,
        None,
        model_name,
        input_path,
        f0up_key,
        f0method,
        index_path,
        index_rate,
        filter_radius,
        resample_sr,
        rms_mix_rate,
        protect,
        opt_path,
    )
    logger.info(f"Cloned vocals audio: {audio}")
    logger.info(f"Cloned vocals audio sr: {sr}")
    logger.info(f"Audio type: {type(audio)}")

    await save_audio_to_wav(audio, "output.wav", sr)

    # Convert numpy array to byte stream
    byte_stream = BytesIO()
    write(byte_stream, sr, np.array(audio, dtype=np.int16))

    # Convert byte stream to Base64 string
    base64_audio = base64.b64encode(byte_stream.getvalue()).decode("utf-8")
    logger.info(
        f"Vocals cloned successfully. Returning Base64 string {base64_audio[:50]}"
    )

    # Close the byte stream
    byte_stream.close()

    return base64_audio
