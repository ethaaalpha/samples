from fastapi.security import OAuth2AuthorizationCodeBearer
from authlib.integrations.starlette_client import OAuth
from authlib.jose import JsonWebKey
import requests

class KeyProvider():
    def __init__(self, url, realm):
        self._key_set = None
        self.target = f"{url}/realms/{realm}/protocol/openid-connect/certs"

    @property
    def key_set(self): # delayed evaluation
        if not self._key_set:
            jwks = requests.get(self.target).json()
            self._key_set = JsonWebKey.import_key_set(jwks)
        return self._key_set

key_provider = KeyProvider("http://keycloak:8082", "hypertube")

def get_key_set():
    return key_provider.key_set

# this will be used to retrieve the token (in the headers) and for the doc
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    tokenUrl="http://keycloak:8082/realms/hypertube/protocol/openid-connect/token?client_id=web",
    authorizationUrl="http://keycloak:8082/realms/hypertube/protocol/openid-connect/auth?client_id=web&response_type=code&scope=email",
    refreshUrl="http://keycloak:8082/realms/hypertube/protocol/openid-connect/token",
    description="the client to use is: web"
)

# since it's an example we rely on the server to exchange auth code with access_token
# but the client can easily handle that
oauth2 = OAuth()
oauth2.register(
    "keycloak",
    client_id="web",
    client_kwargs={"scope": "openid"},
    # we do not use the default scrapper due to localhost/keycloak conflict
    # fastapi can only make request to "keycloak" container name
    # but the authorize_url need to be user readable an then use the "localhost"
    authorize_url="http://localhost:8082/realms/hypertube/protocol/openid-connect/auth",
    access_token_url="http://keycloak:8082/realms/hypertube/protocol/openid-connect/token",
    jwks_uri="http://keycloak:8082/realms/hypertube/protocol/openid-connect/certs",
    userinfo_endpoint="http://keycloak:8082/realms/hypertube/protocol/openid-connect/userinfo"
)
