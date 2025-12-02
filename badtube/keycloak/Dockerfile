FROM quay.io/keycloak/keycloak:26.3.4 AS builder

# Enable health and metrics support
ENV KC_HEALTH_ENABLED=true
ENV KC_METRICS_ENABLED=true
ENV KC_DB=postgres

WORKDIR /opt/keycloak

RUN /opt/keycloak/bin/kc.sh build

FROM quay.io/keycloak/keycloak:26.3.4
COPY --from=builder /opt/keycloak/ /opt/keycloak/
COPY config.sh .

ENTRYPOINT [ "/bin/bash" ]