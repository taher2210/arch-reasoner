#!/bin/bash
# Quick test script for the web app

echo "🧪 Testing Arch Reasoner Web App..."
echo ""

# Check API key
if [ -z "$GEMINI_API_KEY" ]; then
    echo "⚠️  GEMINI_API_KEY not set. Setting it now..."
    export GEMINI_API_KEY='your_api_key_here'
fi

# Test backend
echo "1️⃣  Testing backend..."
cd ~/arch-gemini/backend
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 > /tmp/backend.log 2>&1 &
BACKEND_PID=$!

sleep 3

# Check if backend is running
if curl -s http://localhost:8000/health > /dev/null; then
    echo "   ✅ Backend is running on http://localhost:8000"
else
    echo "   ❌ Backend failed to start"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# Test frontend
echo "2️⃣  Testing frontend..."
cd ~/arch-gemini/frontend
npm run dev > /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!

sleep 5

echo ""
echo "✅ Web app is running!"
echo ""
echo "   🌐 Frontend: http://localhost:3000"
echo "   📡 Backend:  http://localhost:8000"
echo "   📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Trap Ctrl+C
trap "echo ''; echo '🛑 Stopping...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT

wait
