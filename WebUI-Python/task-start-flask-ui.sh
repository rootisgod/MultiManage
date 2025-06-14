#!/bin/bash

# Start FastAPI backend
echo "Starting FastAPI backend..."
cd /Users/iain/Code/Github/MultiManage/WebUI-Python/
./task-start-fastapi.sh

# Start Flask Web UI
echo "Starting Flask Web UI..."
cd /Users/iain/Code/Github/MultiManage/WebUI-Python/web
./start.sh

echo "Services started:"
echo "FastAPI - http://localhost:8001"
echo "Flask UI - http://localhost:5000"
