#!/bin/bash
cd multipass-web
npm run dev >> _nextjs.log 2>&1 &
echo $! > _nextjs.pid
echo "Next.js server started with PID $(cat _nextjs.pid)"
echo "Logs are being written to _nextjs.log"
sleep 1
# Check if the server started successfully
if curl -s http://localhost:3000 > /dev/null; then
    echo "Next.js server is running."
else
    echo "Failed to start Next.js server."
    exit 1
fi