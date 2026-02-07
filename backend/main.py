import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
from ddgs import DDGS
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

app = FastAPI(title="Arch Reasoner API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set")

genai.configure(api_key=API_KEY)

SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

class QueryRequest(BaseModel):
    query: str
    conversation_history: list = []

class QueryResponse(BaseModel):
    answer: str
    source_url: str

def search_arch_wiki(query: str):
    try:
        results = list(DDGS().text(f"site:wiki.archlinux.org {query}", max_results=3))
        if results:
            return results[0]['href']
    except:
        pass
    return None

def get_wiki_content(url: str):
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.content, 'html.parser')
        content_div = soup.find('div', {'id': 'content'}) or soup.find('body')
        text = md(str(content_div), heading_style="ATX")
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch page: {str(e)}")

def ask_gemini(context: str, user_query: str, conversation_history: list):
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Build conversation context
        conv_context = ""
        if conversation_history:
            conv_context = "\n\nPREVIOUS CONVERSATION:\n"
            for msg in conversation_history[-6:]:  # Last 3 exchanges
                conv_context += f"{msg['role'].upper()}: {msg['content']}\n"
        
        prompt = f"""You are a friendly, conversational Arch Linux expert helping beginners.

IMPORTANT RULES:
1. If the user's question is vague or could have multiple solutions, ASK CLARIFYING QUESTIONS first
2. For hardware-specific questions (like GPU drivers), ask what hardware they have
3. Once you have enough info, give ONLY the exact steps they need - no alternatives, no "if you have X do Y"
4. Explain each step in simple terms with WHY it's needed
5. Use the Arch Wiki docs below as reference, but make your answer conversational and personalized
6. Keep responses concise - break complex tasks into digestible steps
7. If they answer your question, use that info to give precise instructions{conv_context}

CURRENT USER MESSAGE: "{user_query}"

ARCH WIKI REFERENCE:
{context}

Remember: Be conversational, ask questions when needed, and give personalized step-by-step guidance."""
        
        response = model.generate_content(prompt, safety_settings=SAFETY_SETTINGS)
        return response.text
    except Exception as e:
        if "quota" in str(e).lower() or "429" in str(e):
            return "⚠️ I've hit my daily API limit. Please try again tomorrow, or set up your own Gemini API key to continue using the service."
        raise e

@app.get("/")
def root():
    return {"message": "Arch Reasoner API", "status": "running"}

@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    # Search Arch Wiki
    url = search_arch_wiki(req.query)
    if not url:
        # If no wiki page found, still try to answer conversationally
        url = "https://wiki.archlinux.org"
        wiki_text = "No specific documentation found. Use your general Arch Linux knowledge."
    else:
        wiki_text = get_wiki_content(url)
    
    answer = ask_gemini(wiki_text, req.query, req.conversation_history)
    
    return QueryResponse(answer=answer, source_url=url)

@app.get("/health")
def health():
    return {"status": "healthy"}
