#!/bin/bash

if [ "$DATABASE_ENGINE" = "postgresql" ]
then
    echo "Waiting for PostgreSQL..."

    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# The Dev Containers extension for Visual Studio Code needs the container
# to be alive. Otherwise, Dev Containers exits with "Stdin closed!".
while sleep 1000; do :; done
exec "$@"