#!/bin/bash

trap 'kill $BACKEND_PID $FRONTEND_PID; exit' SIGINT SIGTERM

echo "Setting up backend..."
cd "$(pwd)/backend"
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi
source venv/bin/activate
pip3 install flask
export FLASK_APP=src/app.py
echo "Running Flask app..."
./src/app.py &
BACKEND_PID=$!

echo "Setting up frontend..."
cd "$(pwd)/../frontend"
if [ ! -d "node_modules" ]; then
  echo "Installing frontend dependencies..."
  npm install
fi
echo "Running frontend app..."
npm run dev &
FRONTEND_PID=$!

wait $BACKEND_PID $FRONTEND_PID
