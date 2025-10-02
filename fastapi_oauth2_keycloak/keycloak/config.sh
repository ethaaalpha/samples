#!/bin/bash

set -e

KADM="kcadm.sh"
REALM="hypertube"
RUNNER="kc.sh"

KEYCLOAK_URL=http://keycloak:8082 

APP_HOST="localhost"

# keycloak recommandation
export PATH=$PATH:$HOME/bin

function credentials {
    ${KADM} config credentials --server ${KEYCLOAK_URL} --realm master --user admin --password admin
}

function configure {
    # configure realm
    ${KADM} create realms -s realm=${REALM} -s enabled=true
    ${KADM} update realms/${REALM} -s registrationAllowed=true
    ${KADM} update realms/${REALM} -s resetPasswordAllowed=true

    # configure smtp server here
    ${KADM} update realms/${REALM} -s smtpServer=\
'{
    "allowutf8" : "",
    "replyToDisplayName" : "",
    "debug" : "false",
    "starttls" : "false",
    "auth" : "",
    "replyTo" : "",
    "host" : "smtp",
    "from" : "no-replay@hypertube.net",
    "fromDisplayName" : "",
    "envelopeFrom" : "",
    "ssl" : "false"
}'

    # create client for app
    ${KADM} create clients -r ${REALM}  -f - << EOF
{
  "clientId": "web",
  "rootUrl": "http://${APP_HOST}:8080/",
  "webOrigins": [ "http://${APP_HOST}:8080/" ],
  "redirectUris": [ "http://${APP_HOST}:8080/auth/*" ],
  "publicClient": "true"
}
EOF

    # create test user
    ${KADM} create users -r ${REALM} -s username=test -s enabled=true -s email=test@example.com -s firstName=test -s lastName=test
    ${KADM} set-password -r ${REALM} --username test --new-password test
}

function waiting {
    until credentials > /dev/null 2>&1; do
        echo "Try keycloak connection (waiting to be ready..)"
        sleep 2
    done
}
function check {
    # waiting perform login inside
    waiting

    if ${KADM} get realms/$REALM > /dev/null 2>&1; then
        echo "Realm '$REALM' already exists."
    else
        echo "Realm '$REALM' does not exist. Starting configuration script.."
        configure
    fi
}

${RUNNER} start --http-enabled=true --hostname=localhost --http-port=8082 --optimized & 
PID=$!

check

echo "Resuming to keycloak PID: ${PID}" 
wait ${PID}
