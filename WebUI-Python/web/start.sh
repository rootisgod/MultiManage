#!/bin/bash

echo "---------- Starting Flask server ----------"

# Stop any existing Flask web server
PID_FILE="_flask.pid"
LOG_FILE="_flask.log"

if [ -f "$PID_FILE" ]; then
    echo "Stopping existing Flask server..."
    kill -9 $(cat "$PID_FILE") 2>/dev/null || true
    rm "$PID_FILE"
fi

# Start Flask server
echo "Starting Flask server..."
nohup python app.py > "$LOG_FILE" 2>&1 &
echo $! > "$PID_FILE"

echo "Flask server started on http://127.0.0.1:5000"
echo "Log file: $LOG_FILE"
echo "PID file: $PID_FILE"
