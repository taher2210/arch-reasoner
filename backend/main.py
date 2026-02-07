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
    allow_credentials=True,
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
    url: str = None

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

def ask_gemini(context: str, user_query: str):
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""You are an Expert Arch Linux Assistant.
I will provide you with a full documentation page from the Arch Wiki.

USER QUESTION: "{user_query}"

INSTRUCTIONS:
1. Answer the question using ONLY the provided context.
2. If the context contains specific commands, list them clearly.
3. If the context mentions configuration files (like /etc/...), specify them.
4. Be concise and technical.
5. Format your response in Markdown.

DOCUMENTATION CONTEXT:
{context}
"""
    
    response = model.generate_content(prompt, safety_settings=SAFETY_SETTINGS)
    return response.text

@app.get("/")
def root():
    return {"message": "Arch Reasoner API", "status": "running"}

@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    if req.url and req.url.startswith('http'):
        url = req.url
    else:
        url = search_arch_wiki(req.query)
        if not url:
            raise HTTPException(status_code=404, detail="No Arch Wiki results found")
    
    wiki_text = get_wiki_content(url)
    answer = ask_gemini(wiki_text, req.query)
    
    return QueryResponse(answer=answer, source_url=url)

@app.get("/health")
def health():
    return {"status": "healthy"}
