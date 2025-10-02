# fast-api + oauth2 support by keycloak server

> [!NOTE]
> only keycloak database is persisted, User table of fastapi are not

technos:
- fastapi (sqlmodel, starlette)
- oauth2 (authlib)
- keycloak

some links:
- https://fastapi.tiangolo.com/reference/security/#fastapi.security.OAuth2AuthorizationCodeBearer
- https://medium.com/@benjaminbuffet/s%C3%A9curiser-fastapi-avec-keycloak-partie-1-5f9847211d3d
- https://www.keycloak.org/docs/latest/server_admin/#admin-cli

add external oidc provider (like github...):
- identity_provider on keycloak, and create mappers if differents names
