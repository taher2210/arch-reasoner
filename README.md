# Arch Assistant

A conversational AI assistant for Arch Linux that helps beginners understand and navigate the Arch Wiki. Built with FastAPI, React, and Google's Gemini AI.

![Arch Assistant](https://img.shields.io/badge/Arch-Linux-1793D1?logo=arch-linux&logoColor=fff)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=fff)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=000)
![Gemini](https://img.shields.io/badge/Gemini-2.5--Flash-4285F4?logo=google&logoColor=fff)

## ✨ Features

### 🤖 Smart Conversational AI
- **Asks clarifying questions** - Instead of overwhelming you with options, it asks what you need
- **Context-aware** - Remembers your conversation to provide personalized guidance
- **Beginner-friendly** - Explains complex concepts in simple terms with step-by-step instructions
- **Explains WHY** - Not just commands, but understanding

### 🎨 Clean Gemini-Style UI
- Minimal, professional design inspired by Google Gemini
- Responsive and mobile-friendly
- Real-time streaming responses
- Markdown rendering with syntax-highlighted code blocks

### 🔧 Technical Features
- FastAPI backend with async support
- React frontend with Vite
- DuckDuckGo search integration for Arch Wiki
- Docker support for easy deployment
- Conversation history for context-aware responses

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Gemini API Key ([Get one free](https://aistudio.google.com/app/apikey))

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

3. **Install backend dependencies:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Install frontend dependencies:**
   ```bash
   cd ../frontend
   npm install
   ```

5. **Start the application:**
   ```bash
   # Terminal 1 - Backend
   cd backend
   source venv/bin/activate
   uvicorn main:app --host 0.0.0.0 --port 8000

   # Terminal 2 - Frontend
   cd frontend
   npm run dev
   ```

6. **Open your browser:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/docs

## 💬 Usage Examples

**Instead of this:**
> "How do I install NVIDIA drivers?"
> 
> *Gets a wall of text with 5 different options for different GPUs*

**You get this:**
> **You:** "How do I install NVIDIA drivers?"
> 
> **Assistant:** "I'd be happy to help! First, what GPU do you have? You can check by running `lspci | grep VGA`"
> 
> **You:** "RTX 3060"
> 
> **Assistant:** "Perfect! For your RTX 3060 (Turing architecture), here's what you need to do:
> 
> 1. Install the driver package:
>    ```bash
>    sudo pacman -S nvidia nvidia-utils
>    ```
>    This installs the proprietary NVIDIA driver which gives you the best performance for gaming and GPU tasks.
> 
> 2. Reboot your system:
>    ```bash
>    sudo reboot
>    ```
>    The driver needs a reboot to load properly.
> 
> That's it! After rebooting, your RTX 3060 will be using the official NVIDIA drivers."

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)
```bash
export GEMINI_API_KEY='your_api_key_here'
docker-compose up -d
```

Access at: http://localhost

### Manual Docker Build
```bash
# Backend
docker build -f Dockerfile.backend -t arch-assistant-backend .
docker run -p 8000:8000 -e GEMINI_API_KEY='your_key' arch-assistant-backend

# Frontend
docker build -f Dockerfile.frontend -t arch-assistant-frontend .
docker run -p 80:80 arch-assistant-frontend
```

## 📁 Project Structure

```
arch-reasoner/
├── backend/              # FastAPI backend
│   ├── main.py          # API endpoints & AI logic
│   ├── requirements.txt # Python dependencies
│   └── venv/            # Virtual environment
├── frontend/            # React frontend
│   ├── src/
│   │   ├── App.jsx     # Main component
│   │   ├── App.css     # Gemini-style UI
│   │   └── main.jsx    # Entry point
│   ├── package.json    # Node dependencies
│   └── vite.config.js  # Vite configuration
├── docker-compose.yml  # Docker orchestration
└── README.md           # This file
```

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

## 🌐 Deployment Options

### Vercel (Frontend)
```bash
cd frontend
npm run build
vercel --prod
```

### Railway/Render (Backend)
1. Connect your GitHub repository
2. Set environment variable: `GEMINI_API_KEY`
3. Deploy from `backend/` directory
4. Update frontend API URL in production

## 🔒 Security

- ✅ API keys stored in environment variables only
- ✅ No credentials in git repository
- ✅ CORS configured for production
- ✅ Input validation on all endpoints
- ⚠️ Add rate limiting for production use

## 📝 API Documentation

### POST /query
Query the Arch Wiki with conversation context

**Request:**
```json
{
  "query": "How do I update my system?",
  "conversation_history": [
    {"role": "user", "content": "previous message"},
    {"role": "assistant", "content": "previous response"}
  ]
}
```

**Response:**
```json
{
  "answer": "To update your Arch system...",
  "source_url": "https://wiki.archlinux.org/title/Pacman"
}
```

### GET /health
Health check endpoint

### GET /docs
Interactive API documentation (Swagger UI)

## 🎨 Customization

### Change Theme
Edit `frontend/src/App.css` and `frontend/src/index.css`

### Change AI Model
Edit `backend/main.py`:
```python
model = genai.GenerativeModel('gemini-2.5-pro')  # Use Pro instead of Flash
```

### Adjust AI Personality
Modify the prompt in `backend/main.py` `ask_gemini()` function

## 🐛 Troubleshooting

**"GEMINI_API_KEY is not set"**
- Export the key: `export GEMINI_API_KEY='your_key'`
- Or add to shell config: `~/.bashrc`, `~/.zshrc`, or `~/.config/fish/config.fish`

**Port already in use:**
```bash
lsof -ti:8000 | xargs kill -9  # Backend
lsof -ti:3000 | xargs kill -9  # Frontend
```

**API quota exceeded:**
- Free tier: 20 requests/day
- Wait 24 hours or use a different API key
- Upgrade to paid tier for higher limits

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - See [LICENSE](LICENSE) file

## 🔗 Links

- [Arch Wiki](https://wiki.archlinux.org/)
- [Gemini API](https://ai.google.dev/)
- [GitHub Repository](https://github.com/taher2210/arch-reasoner)

## 🙏 Acknowledgments

- Arch Linux community for the comprehensive wiki
- Google for the Gemini API
- All contributors and users

---

Made with ⚡ for the Arch Linux community
