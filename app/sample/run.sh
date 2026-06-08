#!/bin/bash
docker stop test_fastapi
docker compose down
docker compose up -d --build
echo "Update completed at $(date)"
