# Arch Reasoner Web App

Production-ready web application for querying the Arch Wiki using AI.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Gemini API Key

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/taher2210/arch-reasoner.git
   cd arch-reasoner
   ```

2. **Set your API key:**
   ```bash
   export GEMINI_API_KEY='your_api_key_here'
   ```

3. **Start the application:**
   ```bash
   ./start.sh
   ```

4. **Open your browser:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## 📁 Project Structure

```
arch-reasoner/
├── backend/              # FastAPI backend
│   ├── main.py          # API endpoints
│   ├── requirements.txt # Python dependencies
│   └── venv/            # Python virtual environment
├── frontend/            # React frontend
│   ├── src/
│   │   ├── App.jsx     # Main component
│   │   ├── App.css     # Styles
│   │   └── main.jsx    # Entry point
│   ├── package.json    # Node dependencies
│   └── vite.config.js  # Vite configuration
├── arch_agent.py       # CLI version
├── ask-arch.sh         # CLI wrapper
└── start.sh            # Startup script
```

## 🎯 Features

### Web Interface
- 💬 Chat-based interface
- 📝 Markdown rendering for responses
- 🔗 Source links to Arch Wiki
- 📱 Responsive design
- ⚡ Real-time streaming responses

### API Endpoints
- `POST /query` - Query the Arch Wiki
- `GET /health` - Health check
- `GET /` - API info

### CLI Tool
- Direct terminal access
- Same AI backend
- Portable script

## 🛠️ Development

### Backend Development
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

### Frontend Development
```bash
cd frontend
npm run dev
```

### Build for Production
```bash
cd frontend
npm run build
```

## 🌐 Deployment

### Docker (Recommended)

**Backend Dockerfile:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Frontend Dockerfile:**
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY frontend/package*.json .
RUN npm install
COPY frontend/ .
RUN npm run build
FROM nginx:alpine
COPY --from=0 /app/dist /usr/share/nginx/html
```

### Deploy to Cloud

**Vercel (Frontend):**
```bash
cd frontend
npm run build
vercel --prod
```

**Railway/Render (Backend):**
- Connect GitHub repo
- Set `GEMINI_API_KEY` environment variable
- Deploy from `backend/` directory

## 🔒 Security

- API key stored in environment variables
- CORS configured for production
- Input validation on all endpoints
- Rate limiting recommended for production

## 📝 API Usage

### Query Endpoint
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How to install NVIDIA drivers?",
    "url": null
  }'
```

### Response
```json
{
  "answer": "To install NVIDIA drivers...",
  "source_url": "https://wiki.archlinux.org/title/NVIDIA"
}
```

## 🎨 Customization

### Change Theme
Edit `frontend/src/App.css` - modify gradient colors:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Change Model
Edit `backend/main.py`:
```python
model = genai.GenerativeModel('gemini-2.5-pro')  # Use Pro instead of Flash
```

## 🐛 Troubleshooting

**Backend won't start:**
- Check if port 8000 is available
- Verify GEMINI_API_KEY is set
- Check Python version (3.8+)

**Frontend won't start:**
- Check if port 3000 is available
- Run `npm install` again
- Clear node_modules and reinstall

**API errors:**
- Verify API key is valid
- Check internet connection
- Review backend logs

## 📄 License

MIT License - See LICENSE file

## 🤝 Contributing

Contributions welcome! Please open an issue or PR.

## 🔗 Links

- [Arch Wiki](https://wiki.archlinux.org/)
- [Gemini API](https://ai.google.dev/)
- [GitHub Repository](https://github.com/taher2210/arch-reasoner)
