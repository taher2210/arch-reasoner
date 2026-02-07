import { useState } from 'react'
import axios from 'axios'
import ReactMarkdown from 'react-markdown'
import './App.css'

function App() {
  const [query, setQuery] = useState('')
  const [url, setUrl] = useState('')
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!query.trim()) return

    const userMessage = { role: 'user', content: query }
    setMessages(prev => [...prev, userMessage])
    setLoading(true)

    try {
      const response = await axios.post('/api/query', {
        query: query,
        url: url || null
      })

      const botMessage = {
        role: 'assistant',
        content: response.data.answer,
        source: response.data.source_url
      }
      setMessages(prev => [...prev, botMessage])
    } catch (error) {
      const errorMessage = {
        role: 'error',
        content: error.response?.data?.detail || 'Failed to get response. Please try again.'
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
      setQuery('')
      setUrl('')
    }
  }

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1>🐧 Arch Reasoner</h1>
          <p>AI-Powered Arch Wiki Assistant</p>
        </header>

        <div className="chat-container">
          <div className="messages">
            {messages.length === 0 && (
              <div className="welcome">
                <h2>Welcome to Arch Reasoner!</h2>
                <p>Ask me anything about Arch Linux. I'll search the official Arch Wiki and provide detailed answers.</p>
                <div className="examples">
                  <h3>Try asking:</h3>
                  <ul>
                    <li>"How do I install NVIDIA drivers?"</li>
                    <li>"How to update my system with pacman?"</li>
                    <li>"Setup Bluetooth on Arch Linux"</li>
                  </ul>
                </div>
              </div>
            )}

            {messages.map((msg, idx) => (
              <div key={idx} className={`message ${msg.role}`}>
                {msg.role === 'user' && <div className="avatar">👤</div>}
                {msg.role === 'assistant' && <div className="avatar">🤖</div>}
                {msg.role === 'error' && <div className="avatar">⚠️</div>}
                
                <div className="message-content">
                  {msg.role === 'assistant' ? (
                    <>
                      <ReactMarkdown>{msg.content}</ReactMarkdown>
                      {msg.source && (
                        <div className="source">
                          📚 Source: <a href={msg.source} target="_blank" rel="noopener noreferrer">{msg.source}</a>
                        </div>
                      )}
                    </>
                  ) : (
                    <p>{msg.content}</p>
                  )}
                </div>
              </div>
            ))}

            {loading && (
              <div className="message assistant">
                <div className="avatar">🤖</div>
                <div className="message-content">
                  <div className="typing">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
          </div>

          <form className="input-form" onSubmit={handleSubmit}>
            <input
              type="text"
              className="url-input"
              placeholder="Optional: Direct Arch Wiki URL"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
            />
            <div className="query-row">
              <input
                type="text"
                className="query-input"
                placeholder="Ask about Arch Linux..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                disabled={loading}
              />
              <button type="submit" disabled={loading || !query.trim()}>
                {loading ? '⏳' : '🚀'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}

export default App
