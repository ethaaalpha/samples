from functools import cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # load from actual environnement, see SettingsConfigDict for .env
    tmdb_key: str
    jackett_key: str
    jackett_host: str
    opensubtitles_key: str
    opensubtitles_app: str

    downloads_location: str

    local_db: bool = False
    db_host: str
    db_username: str
    db_password: str
    db_name: str

    keycloak_url: str
    keycloak_realm: str

@cache
def get_settings():
    # singleton
    return Settings()
