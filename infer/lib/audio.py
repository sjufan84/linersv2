import platform
import ffmpeg
import numpy as np
import av
import tempfile
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

def load_audio(audio_bytes, sr):
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
            # Write the audio bytes to the temporary file
            temp_audio.write(audio_bytes)
            temp_audio_path = temp_audio.name

        # Pass the path of the temporary file to ffmpeg
        out, _ = (
            ffmpeg.input(temp_audio_path)
            .output("pipe:", format="f32le", acodec="pcm_f32le", ac=1, ar=sr)
            .run(capture_stdout=True, capture_stderr=True)
        )

        audio_array = np.frombuffer(out, np.float32)
        logger.info(f"{audio_array[:1]}")
        return audio_array

    except Exception as e:
        raise RuntimeError(f"Failed to load audio: {e}")

def clean_path(path_str):
    if platform.system() == "Windows":
        path_str = path_str.replace("/", "\\")
    return path_str.strip(" ").strip('"').strip("\n").strip('"').strip(" ")
