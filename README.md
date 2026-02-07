# Arch-Reasoner - Long-Context Arch Wiki Agent

A CLI tool that searches the Arch Wiki, scrapes documentation pages, and uses Google's Gemini 2.5 Flash to answer your questions based on the official documentation.

## Features

- 🔍 Direct Arch Wiki page scraping
- 🤖 Powered by Gemini 2.5 Flash (long-context model)
- 📝 Converts HTML to clean Markdown for efficient token usage
- 🎨 Rich terminal output with streaming responses
- ⚡ No pagination needed - handles entire wiki pages

## Prerequisites

- Python 3.8+
- Arch Linux (or any Linux distribution)
- Google Gemini API key ([Get one free here](https://aistudio.google.com/app/apikey))

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/arch-reasoner.git
   cd arch-reasoner
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API key:**
   
   Add to your shell config (`~/.bashrc`, `~/.zshrc`, or `~/.config/fish/config.fish`):
   
   **Bash/Zsh:**
   ```bash
   export GEMINI_API_KEY='your_api_key_here'
   ```
   
   **Fish:**
   ```fish
   set -gx GEMINI_API_KEY 'your_api_key_here'
   ```

5. **Make the wrapper script executable:**
   ```bash
   chmod +x ask-arch.sh
   ```

6. **Create an alias (optional but recommended):**
   
   **Bash/Zsh** (`~/.bashrc` or `~/.zshrc`):
   ```bash
   alias ask-arch='~/arch-reasoner/ask-arch.sh'
   ```
   
   **Fish** (`~/.config/fish/config.fish`):
   ```fish
   alias ask-arch='~/arch-reasoner/ask-arch.sh'
   ```

7. **Reload your shell:**
   ```bash
   source ~/.bashrc  # or ~/.zshrc or ~/.config/fish/config.fish
   ```

## Usage

### Direct URL Mode (Recommended)
```bash
ask-arch https://wiki.archlinux.org/title/NVIDIA
```

### Direct URL + Custom Question
```bash
ask-arch https://wiki.archlinux.org/title/NVIDIA 'how do I install nvidia drivers'
```

### Search Mode
```bash
ask-arch 'nvidia installation'
```
*Note: DuckDuckGo search may be rate-limited. Use direct URLs for reliability.*

## Examples

```bash
# System updates
ask-arch https://wiki.archlinux.org/title/Pacman 'how to update system'

# Service management
ask-arch https://wiki.archlinux.org/title/Systemd 'how to enable a service'

# Bluetooth setup
ask-arch https://wiki.archlinux.org/title/Bluetooth 'setup bluetooth'

# Network configuration
ask-arch https://wiki.archlinux.org/title/NetworkManager 'configure wifi'
```

## Popular Arch Wiki URLs

- **NVIDIA Drivers**: https://wiki.archlinux.org/title/NVIDIA
- **Pacman**: https://wiki.archlinux.org/title/Pacman
- **Systemd**: https://wiki.archlinux.org/title/Systemd
- **Bluetooth**: https://wiki.archlinux.org/title/Bluetooth
- **NetworkManager**: https://wiki.archlinux.org/title/NetworkManager
- **AUR**: https://wiki.archlinux.org/title/Arch_User_Repository

## How It Works

1. **Search/Fetch**: Searches Arch Wiki via DuckDuckGo or uses direct URL
2. **Scrape**: Fetches the HTML content and converts to Markdown
3. **Reason**: Sends the full page context to Gemini 2.5 Flash
4. **Stream**: Displays the AI response in real-time with rich formatting

## Configuration

- **Model**: `gemini-2.5-flash` (latest available)
- **Safety Settings**: All set to `BLOCK_NONE` to prevent false positives on technical terms
- **Context Window**: Handles entire Arch Wiki pages without truncation

## Troubleshooting

**"GEMINI_API_KEY is not set" error:**
- Make sure you've exported the API key in your shell config
- Reload your shell: `source ~/.bashrc` (or equivalent)

**Search returns no results:**
- Use direct URLs instead: `ask-arch https://wiki.archlinux.org/title/PAGE_NAME`

**API errors:**
- Verify your API key is valid at https://aistudio.google.com/app/apikey
- Check your internet connection

## Dependencies

- `google-generativeai` - Gemini API client
- `duckduckgo-search` - Web search
- `requests` - HTTP client
- `beautifulsoup4` - HTML parsing
- `markdownify` - HTML to Markdown conversion
- `rich` - Terminal formatting

## License

MIT License - Feel free to use and modify!

## Contributing

Contributions welcome! Feel free to open issues or submit pull requests.

## Disclaimer

This tool scrapes the Arch Wiki for educational purposes. Always refer to the official Arch Wiki for the most up-to-date information.
