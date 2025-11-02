#!/bin/bash
set -e

wait_for_db() {
    if [ -z "$DATABASE_HOST" ]; then
        echo "DATABASE_HOST not set, skipping database wait"
        return 0
    fi

    echo "Waiting for database at $DATABASE_HOST:$DATABASE_PORT..."
    local timeout=30
    local counter=0

    while ! nc -z "$DATABASE_HOST" "$DATABASE_PORT"; do
        sleep 1
        counter=$((counter + 1))
        if [ $counter -ge $timeout ]; then
            echo "❌ Timeout: Database not available after $timeout seconds"
            exit 1
        fi
    done
    echo "✅ Database is ready!"
}

# Only run setup for Gunicorn/Daphne
if [ "$1" = "gunicorn" ] || [ "$1" = "daphne" ]; then
    echo "------------------------------------------"
    echo "🛠️  Running Django setup commands..."
    echo "------------------------------------------"

    wait_for_db

    if [ ! -f "manage.py" ]; then
        echo "❌ manage.py not found — check your app directory."
        exit 1
    fi

    echo "📦 Applying migrations..."
    python manage.py migrate --noinput

    if [ "$DEBUG" != "True" ]; then
        echo "📁 Collecting static files..."
        python manage.py collectstatic --noinput
    else
        echo "⚙️  DEBUG=True, skipping collectstatic"
    fi

    echo "💾 Creating cache table (if applicable)..."
    python manage.py createcachetable || echo "Cache table creation skipped"

    echo "✅ Django setup complete!"
    echo "------------------------------------------"
fi

echo "🚀 Starting: $@"
exec "$@"
