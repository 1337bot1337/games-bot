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
    python /src/api/manage.py makemigrations
    python /src/api/manage.py migrate --noinput
    python /src/api/manage.py init_botprofiles
    python /src/api/manage.py update_cache
#    python /src/api/manage.py makemigrations account
#    python /src/api/manage.py migrate account

fi

exec "$@"
