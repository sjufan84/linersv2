import platform
import ffmpeg
import numpy as np
import av
import tempfile
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def wav2(i, o, format):
    inp = av.open(i, "r")
    if format == "m4a":
        format = "mp4"
    out = av.open(o, "w", format=format)
    if format == "ogg":
        format = "libvorbis"
    if format == "mp4":
        format = "aac"

    ostream = out.add_stream(format)

    for frame in inp.decode(audio=0):
        for p in ostream.encode(frame):
            out.mux(p)

    for p in ostream.encode(None):
        out.mux(p)

    out.close()
    inp.close()


def load_audio(file, sr):
    try:
        # https://github.com/openai/whisper/blob/main/whisper/audio.py#L26
        # This launches a subprocess to decode audio while down-mixing and resampling as necessary.
        # Requires the ffmpeg CLI and `ffmpeg-python` package to be installed.
        temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        temp_file.close()
        with open(temp_file.name, "wb") as f:
            f.write(file.file.read())
        file = temp_file.name
        file = clean_path(file)

        logger.info(f"Loading audio file: {file} with size {os.path.getsize(file)}")

        out, _ = (
            ffmpeg.input(file, threads=0)
            .output("-", format="f32le", acodec="pcm_f32le", ac=1, ar=sr)
            .run(cmd=["ffmpeg", "-nostdin"], capture_stdout=True, capture_stderr=True)
        )
        # Log the unique values in the array
        logger.info(f"Unique values in audio array: {len(np.unique(np.frombuffer(out, np.float32)))}")

        # Clean up the temporary file
        os.remove(file)
        
    except Exception as e:
        raise RuntimeError(f"Failed to load audio: {e}")

    return np.frombuffer(out, np.float32).flatten()


def clean_path(path_str):
    if platform.system() == "Windows":
        path_str = path_str.replace("/", "\\")
    return path_str.strip(" ").strip('"').strip("\n").strip('"').strip(" ")