#!/bin/bash
set -e

echo "waiting for database to be ready..."

DB_URL=${MIGRATE_URL:-$DATABASE_URL}
if [ -z "$DB_URL" ]; then
    echo "Error: Neither DATABASE_URL nor MIGRATE_URL environment variable is set"
    exit 1
fi

DB_HOST=$(echo $DB_URL | sed -n 's|.*://[^@]*@\([^:]*\):.*|\1|p')
DB_PORT=$(echo $DB_URL | sed -n 's|.*://[^@]*@[^:]*:\([0-9]*\)/.*|\1|p')
DB_USER=$(echo $DB_URL | sed -n 's|.*://\([^:]*\):.*@.*|\1|p')


DB_HOST=${DB_HOST:-db}
DB_PORT=${DB_PORT:-5432}
DB_USER=${DB_USER:-yixin}

echo "Connecting to database at $DB_HOST:$DB_PORT with user $DB_USER"

# Wait for the database to be ready
while ! pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER; do
    echo "Database is not ready, waiting 1 seconds..."
    sleep 1
done

echo "Database is ready, running migrations..."
uv run alembic upgrade head

echo "Starting FastAPI application..."
exec uv run uvicorn app.main:app --host 0.0.0.0 --port 8000