#!/bin/bash
source venv/bin/activate
nohup uvicorn main:app --host 0.0.0.0 --port 8000 --reload >> _fastapi.log 2>&1 &
echo $! > _fastapi.pid
echo "FastAPI server started with PID $(cat _fastapi.pid)"
echo "Logs are being written to _fastapi.log"
sleep 2
# Check if the server started successfully
if curl -s http://localhost:8000 > /dev/null; then
    echo "FastAPI server is running."
else
    echo "Failed to start FastAPI server."
    exit 1
fi