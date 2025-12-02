from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from controllers.streaming import StreamingServiceInj
from controllers.torrent.converter import stream_video
from objects.movie import Movie
from objects.torrent_file import TorrentFile
from routes.tools.dependencies import get_movie, get_torrent_file

router = APIRouter(prefix="/stream", tags=["streaming"], responses={404: {"description": "The movie/torrent do not exist!"}})

@router.get("/{movie_id}/play", description="Request download/preparation of movie for streaming.")
async def play(movie: Annotated[Movie, Depends(get_movie)], service: StreamingServiceInj):
    return await service.play(movie)

@router.get("/{movie_id}/status", description="See if a movie is already for streaming.")
def status(movie: Annotated[Movie, Depends(get_movie)], service: StreamingServiceInj): 
    return service.status(movie)

@router.get("/{movie_id}/raw", description="Get the raw bytes for video player!")
def raw(torrent_file: Annotated[TorrentFile, Depends(get_torrent_file)]):
    return StreamingResponse(stream_video(torrent_file), media_type="video/mp4")
