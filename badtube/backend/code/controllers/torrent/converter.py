import logging
from pathlib import Path
from subprocess import PIPE, Popen
from typing import Generator
from fastapi import HTTPException
from controllers.torrent.files import get_torrent_directory
from objects.torrent_file import TorrentFile

BUFFER_SIZE = 4096
NATIVES_EXT = [".webm", ".mp4"]

logger = logging.getLogger(__name__)

def serve(path: Path) -> Generator[bytes, None]:
    with open(path, "rb") as file:
        while True:
            part = file.read(BUFFER_SIZE)

            if not part:
                break
            yield part

def convert(path: Path) -> Generator[bytes, None]:
    # this convert files to mp4 using ffmpeg
    # the data is streamed threw a PIPE
    # frag_keyframe+empty_moov are to allow video player
    # to stream data without having to wait the whole file
    # to read the metadata MOOV (it's required for playing mp4)
    cmd = [
        "ffmpeg",
        "-i", path,
        "-c:a", "aac",
        "-c:v", "libx264",
        "-movflags", "frag_keyframe+empty_moov",
        "-f", "mp4",
        "pipe:1"
    ]

    process = Popen(cmd, stdout=PIPE, stderr=PIPE, bufsize=BUFFER_SIZE)
    try:
        while True:
            part = process.stdout.read(BUFFER_SIZE)

            if not part:
                # end of pipe
                # this could be natural or a fail or converting
                break
            yield part
    except GeneratorExit:
        if process.poll() is None:
            # we could wait but that's okay to kill
            process.kill()
            process.wait()
    finally:
        process.stdout.close()
        process.wait(timeout=5)

        if process.returncode != 0:
            print(f"{process.stderr.read().decode(errors="ignore")}")
            raise HTTPException(400, "The content failed to be played!")

        process.stderr.close()

def stream_video(file: TorrentFile) -> Generator[bytes, None]:
    path = get_torrent_directory(file.torrent.movie.id).joinpath(f"movie{file.ext}").resolve()

    if file.ext in NATIVES_EXT:
        return serve(path)
    else:
        return convert(path)
