#!/usr/bin/env bash

set -e

RUN_MANAGE_PY='poetry run python3 -m core.manage'

echo 'Collecting static files...'
$RUN_MANAGE_PY collectstatic --no-input

echo 'Running makemigrations...'
$RUN_MANAGE_PY makemigrations

echo 'Running migrations...'
$RUN_MANAGE_PY migrate --no-input

exec $RUN_MANAGE_PY runserver 0.0.0.0:8000

