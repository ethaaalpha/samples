-- since we share the DB between two services,
-- this helps us avoid database colision
CREATE SCHEMA IF NOT EXISTS fastapi;
CREATE SCHEMA IF NOT EXISTS keycloak;
