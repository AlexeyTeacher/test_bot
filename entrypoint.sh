#!/usr/bin/env bash
set -e

python3 /app/upgrade_alembic.py
python3 /app/main.py