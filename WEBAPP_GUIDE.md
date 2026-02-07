# 🚀 ARCH REASONER WEB APP - READY TO USE!

## ✅ What's Been Built

A production-ready web application with:
- **FastAPI Backend** - RESTful API with Gemini AI integration
- **React Frontend** - Beautiful chat interface with markdown support
- **Docker Support** - Easy deployment with docker-compose
- **Full Documentation** - Setup guides and API docs

## 🎯 Quick Start (3 Steps)

### 1. Set API Key
```bash
export GEMINI_API_KEY='your_api_key_here'
```

### 2. Start the App
```bash
cd ~/arch-gemini
./start.sh
```

### 3. Open Browser
Go to: **http://localhost:3000**

That's it! 🎉

## 📱 What You Get

### Web Interface (http://localhost:3000)
- Beautiful chat UI with purple gradient theme
- Real-time AI responses
- Markdown formatting for code and commands
- Source links to Arch Wiki
- Mobile responsive design

### API (http://localhost:8000)
- RESTful endpoints
- Auto-generated docs at `/docs`
- CORS enabled for frontend
- Health check endpoint

### CLI Tool (Still Works!)
```bash
ask-arch 'how to install nvidia'
```

## 🐳 Docker Deployment

### Option 1: Docker Compose (Easiest)
```bash
cd ~/arch-gemini
export GEMINI_API_KEY='your_key'
docker-compose up -d
```
Access at: http://localhost

### Option 2: Manual Docker
```bash
# Backend
docker build -f Dockerfile.backend -t arch-reasoner-backend .
docker run -p 8000:8000 -e GEMINI_API_KEY='your_key' arch-reasoner-backend

# Frontend
docker build -f Dockerfile.frontend -t arch-reasoner-frontend .
docker run -p 80:80 arch-reasoner-frontend
```

## 🌐 Deploy to Cloud

### Vercel (Frontend)
```bash
cd frontend
npm run build
vercel --prod
```

### Railway/Render (Backend)
1. Connect GitHub repo
2. Set environment variable: `GEMINI_API_KEY`
3. Deploy from `backend/` directory
4. Update frontend API URL in `vite.config.js`

## 📁 Project Structure

```
arch-gemini/
├── backend/
│   ├── main.py              # FastAPI app
│   ├── requirements.txt     # Python deps
│   └── venv/               # Virtual env
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main React component
│   │   ├── App.css         # Styles
│   │   └── main.jsx        # Entry point
│   ├── package.json        # Node deps
│   └── vite.config.js      # Vite config
├── start.sh                # Start both servers
├── test.sh                 # Test script
├── docker-compose.yml      # Docker orchestration
├── Dockerfile.backend      # Backend container
└── Dockerfile.frontend     # Frontend container
```

## 🎨 Features

### Chat Interface
- ✅ Real-time streaming responses
- ✅ Markdown rendering (code blocks, lists, links)
- ✅ Message history
- ✅ Loading animations
- ✅ Error handling
- ✅ Source attribution

### API Features
- ✅ Search Arch Wiki automatically
- ✅ Direct URL support
- ✅ Gemini 2.5 Flash integration
- ✅ Safety settings configured
- ✅ CORS enabled
- ✅ Health checks

## 🔧 Customization

### Change Theme Colors
Edit `frontend/src/App.css`:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Change AI Model
Edit `backend/main.py`:
```python
model = genai.GenerativeModel('gemini-2.5-pro')
```

### Change Ports
Edit `start.sh`:
```bash
--port 8000  # Backend
port: 3000   # Frontend (in vite.config.js)
```

## 🐛 Troubleshooting

**Port already in use:**
```bash
# Kill processes on ports
lsof -ti:8000 | xargs kill -9
lsof -ti:3000 | xargs kill -9
```

**Backend won't start:**
- Check `GEMINI_API_KEY` is set
- Verify Python 3.8+
- Check backend logs: `tail -f /tmp/backend.log`

**Frontend won't start:**
- Run `npm install` in frontend/
- Check Node.js 16+
- Clear cache: `rm -rf node_modules package-lock.json && npm install`

## 📊 API Endpoints

### POST /query
Query the Arch Wiki
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "install nvidia", "url": null}'
```

### GET /health
Health check
```bash
curl http://localhost:8000/health
```

### GET /docs
Interactive API documentation (Swagger UI)

## 🔒 Security Notes

- ✅ API key in environment variables only
- ✅ No credentials in git
- ✅ CORS configured
- ✅ Input validation
- ⚠️ Add rate limiting for production
- ⚠️ Use HTTPS in production

## 📝 Next Steps

1. **Test locally**: `./start.sh`
2. **Customize theme**: Edit CSS files
3. **Deploy**: Use Docker or cloud platforms
4. **Add features**: Authentication, history, etc.

## 🎉 You're Done!

Your production-ready Arch Wiki chatbot is complete!

**GitHub**: https://github.com/taher2210/arch-reasoner
**Local**: http://localhost:3000

Enjoy! 🐧
