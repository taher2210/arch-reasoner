import os
import sys
import requests
import google.generativeai as genai
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()

# 1. AUTH
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    console.print("[bold red]❌ Error:[/bold red] GEMINI_API_KEY is not set.")
    console.print("Please export it: export GEMINI_API_KEY='your_key_here'")
    sys.exit(1)

genai.configure(api_key=API_KEY)

# Safety settings to prevent blocking technical terms (like 'kill process')
SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

def search_arch_wiki(query):
    """Finds the best Arch Wiki URL."""
    console.print(f"[dim]🔍 Searching Arch Wiki for: {query}...[/dim]")
    try:
        results = DDGS().text(f"site:wiki.archlinux.org {query}", max_results=3)
        if results:
            return results[0]['href']
    except Exception as e:
        console.print(f"[yellow]Search failed: {e}[/yellow]")
    return None

def get_wiki_content(url):
    """Fetches and converts Wiki HTML to clean Markdown."""
    console.print(f"[dim]⬇️  Fetching: {url}[/dim]")
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(resp.content, 'html.parser')
        content_div = soup.find('div', {'id': 'content'}) or soup.find('body')
        
        # Convert to Markdown to save tokens and keep structure
        text = md(str(content_div), heading_style="ATX")
        return text
    except Exception as e:
        console.print(f"[red]Failed to fetch page: {e}[/red]")
        return None

def ask_gemini(context, user_query):
    """Sends the context + query to Gemini 1.5 Flash."""
    console.print("[bold green]🧠 Gemini is reading the documentation...[/bold green]")
    
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""
You are an Expert Arch Linux Assistant.
I will provide you with a full documentation page from the Arch Wiki.

USER QUESTION: "{user_query}"

INSTRUCTIONS:
1. Answer the question using ONLY the provided context.
2. If the context contains specific commands, list them clearly.
3. If the context mentions configuration files (like /etc/...), specify them.
4. Be concise and technical.

DOCUMENTATION CONTEXT:
{context}
"""
    
    try:
        response = model.generate_content(
            prompt,
            safety_settings=SAFETY_SETTINGS,
            stream=True
        )
        
        console.print("\n")
        console.print(Panel(f"[bold]Query:[/bold] {user_query}", style="cyan"))
        
        # Stream the output for a chat-like feel
        full_text = ""
        for chunk in response:
            if chunk.text:
                print(chunk.text, end="", flush=True)
                full_text += chunk.text
        print("\n")
    except Exception as e:
        console.print(f"[red]Gemini API Error: {e}[/red]")
        console.print("[yellow]Check your API key or try: gemini-1.5-pro-latest[/yellow]")

def main():
    if len(sys.argv) < 2:
        console.print("[yellow]Usage:[/yellow] ask-arch 'how to install nvidia drivers'")
        console.print("[yellow]   or:[/yellow] ask-arch https://wiki.archlinux.org/title/NVIDIA 'custom question'")
        sys.exit(1)
        
    # Check if first arg is URL
    if sys.argv[1].startswith('http'):
        url = sys.argv[1]
        query = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else "Explain this page"
        console.print(f"[bold blue]Using URL:[/bold blue] {url}")
    else:
        query = ' '.join(sys.argv[1:])
        # Search
        url = search_arch_wiki(query)
        if not url:
            console.print("[red]No Arch Wiki results found.[/red]")
            console.print("[yellow]Try using a direct URL instead:[/yellow]")
            console.print("  ask-arch https://wiki.archlinux.org/title/NVIDIA")
            return
            
        console.print(f"[bold blue]found:[/bold blue] {url}")
    
    # Extract
    wiki_text = get_wiki_content(url)
    if not wiki_text:
        return
        
    # Reason
    ask_gemini(wiki_text, query)

if __name__ == "__main__":
    main()
