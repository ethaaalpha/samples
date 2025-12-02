from os import makedirs
import os
from pathlib import Path
from shutil import rmtree
from objects.enum.language import Language
from settings import get_settings

SUBTITLES_FOLDER="42subtitles"
MOVIE_BASENAME="movie"

def _movie_dir(movie_id: str) -> Path:
    settings = get_settings()

    return Path(f"{settings.downloads_location}/{movie_id}")

def create_torrent_directory(movie_id: str) -> Path:
    path = _movie_dir(movie_id)
    makedirs(path.resolve(), exist_ok=True)
    makedirs(path.joinpath(SUBTITLES_FOLDER).resolve(), exist_ok=True)

    return path

def delete_torrent_directory(movie_id: str):
    path = _movie_dir(movie_id)
    rmtree(path)

def get_torrent_directory(movie_id: str) -> Path:
    return _movie_dir(movie_id).resolve()

def clean_torrent_directory(movie_id: str):
    """will ensure that the directory only contain subtitles and movie file"""
    path = _movie_dir(movie_id)

    files = os.listdir(path)

    for file in files:
        file_path = path.joinpath(file)

        if file == SUBTITLES_FOLDER and os.path.isdir(file_path):
            continue
        elif os.path.basename(file) == MOVIE_BASENAME:
            continue
        else:
            rmtree(file_path)

def get_subtitle_file(movie_id: str, lang: Language) -> Path:
    return _movie_dir(movie_id).joinpath(SUBTITLES_FOLDER).joinpath(f"{lang.value}.vtt").resolve()
