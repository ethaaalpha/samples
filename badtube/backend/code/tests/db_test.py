from datetime import date, datetime
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, StaticPool, create_engine
import pytest
import app
from controllers.dao.objects import get_movie_service, get_torrent_service
from objects.enum.language import Language
from objects.movie import Movie
from objects.subtitle import SubtitleFile
from objects.torrent import Torrent
from objects.torrent_file import TorrentFile

client = TestClient(app.app)

@pytest.fixture(name="session")  
def session_fixture():  
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session  

def test_movie(session: Session):
    service = get_movie_service(session)

    movie = Movie(id=1, title="test", desc="test", release_date=date.today(), rating=3.3, img_link="test")
    service.upsert(movie)

    assert service.get(1) == movie

    movie.id = 2
    service.upsert(movie)
    assert service.get(1) is None
    assert service.get(2) == movie

def test_movie_and_torrent(session: Session):
    m_service = get_movie_service(session)
    t_service = get_torrent_service(session)

    movie = Movie(id=1, title="test", desc="test", release_date=date.today(), rating=3.3, img_link="test")
    torrent = Torrent(url="test", peers=2, seeders=2)

    # creation and link
    movie.torrent = torrent
    m_service.upsert(movie)
    assert m_service.get(1).torrent == torrent
    assert t_service.all().pop().movie == movie

    # delete
    m_service.delete(movie)
    assert len(m_service.all()) == 0
    # cascade relation-ship effect
    assert len(t_service.all()) == 0

    # create and link but reverse order
    movie = Movie(id="1", title="test", desc="test", release_date=date.today(), rating=3.3, img_link="test")
    torrent = Torrent(url="test", peers=2, seeders=2)

    torrent.movie = movie
    t_service.upsert(torrent)
    assert m_service.get(1).torrent == torrent
    assert t_service.all().pop().movie == movie

def test_complex_object(session: Session):
    service = get_movie_service(session)

    movie = Movie(id=1, title="test", desc="test", release_date=date.today(), rating=3.3, img_link="test")
    torrent = Torrent(url="test", peers=2, seeders=2)
    file = TorrentFile(completed=False, hash="muette", ext=".ext", last_watched=datetime.now())
    subtitles = [
        SubtitleFile(language=Language.FR),
        SubtitleFile(language=Language.EN)
    ]

    torrent.file = file
    torrent.subtitles = subtitles
    movie.torrent = torrent

    service.upsert(movie)
    db_movie = service.get(movie.id)

    # since objects where refreshed we call parents
    # (they expired after flushing)
    assert db_movie.torrent.file == torrent.file
    assert db_movie.torrent.subtitles == torrent.subtitles
    assert db_movie.torrent == torrent
    assert db_movie == movie
