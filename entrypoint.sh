#!/bin/sh
set -e

echo "Running migrations..."
alembic upgrade head

echo "Starting FastAPI app..."
exec uvicorn app.main:app --reload --host 0.0.0.0
