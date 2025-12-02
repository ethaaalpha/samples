FROM lscr.io/linuxserver/jackett:0.24.250
# anonymous volume inside image for /config

RUN apk add --no-cache envsubst

WORKDIR /app

RUN mkdir -p indexers

COPY indexers/* indexers/
COPY config.template.json .
COPY entrypoint.sh .

ENTRYPOINT [ "/bin/bash", "entrypoint.sh" ]
