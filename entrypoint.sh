#!/bin/bash
set -e

echo "waiting for database to be ready..."
# Wait for the database to be ready
while ! pg_isready -h postgres -p 5432 -U yixin; do
    echo "Database is not ready, waiting 2 seconds..."
    sleep 2
done

echo "Database is ready, running migrations..."
alembic upgrade head

echo "Starting FastAPI application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000