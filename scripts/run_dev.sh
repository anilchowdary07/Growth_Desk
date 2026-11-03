#!/usr/bin/env bash
set -e

echo "=================================================="
echo "🚀 Launching AI GrowthDesk Development Environment"
echo "=================================================="

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Start Backend
echo "Starting FastAPI Backend on http://localhost:8000..."
cd "$ROOT_DIR/backend"
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Start Frontend
echo "Starting Next.js Frontend on http://localhost:3000..."
cd "$ROOT_DIR/frontend"
npm run dev &
FRONTEND_PID=$!

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" SIGINT SIGTERM

echo "=================================================="
echo "AI GrowthDesk is running!"
echo "👉 Frontend: http://localhost:3000"
echo "👉 API Docs: http://localhost:8000/docs"
echo "Press Ctrl+C to stop all servers."
echo "=================================================="

wait
