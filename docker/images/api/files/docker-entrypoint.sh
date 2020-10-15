#!/bin/bash

# Stop on errors
set -eo pipefail

if [ "CORE_DATABASE_WAIT" ]; then
    while true
    do
        if python /src/docker/wait_for_dependencies.py
        then
            break
        fi
        echo 'Database is unavailable - sleeping'
        sleep 1
    done
fi

if [ "CORE_DATABASE_WAIT" ]; then
    python /src/api/manage.py migrate --noinput
    python /src/api/manage.py makemigrations game
    python /src/api/manage.py migrate game
fi

exec "$@"
