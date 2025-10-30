#!/usr/bin/env sh
set -e

HOST="${DB_HOST:-127.0.0.1}"
PORT="${DB_PORT:-5432}"
USER="${DB_USER:-postgres}"
NAME="${DB_NAME:-postgres}"

echo "Aguardando Postgres em $HOST:$PORT (db=$NAME user=$USER)..."

# tente por até ~60s
i=0
while ! pg_isready -h "$HOST" -p "$PORT" -U "$USER" -d "$NAME" >/dev/null 2>&1; do
  i=$((i+1))
  if [ "$i" -ge 60 ]; then
    echo "Postgres não respondeu a tempo."
    exit 1
  fi
  sleep 1
done

echo "Postgres OK."
