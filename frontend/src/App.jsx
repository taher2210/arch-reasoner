import { useState } from 'react'
import axios from 'axios'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import './App.css'

function App() {
  const [query, setQuery] = useState('')
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!query.trim()) return

    const currentQuery = query
    
    const userMessage = { role: 'user', content: currentQuery }
    const newMessages = [...messages, userMessage]
    setMessages(newMessages)
    setQuery('')
    setLoading(true)

    try {
      // Build conversation history for context
      const conversationHistory = newMessages.map(msg => ({
        role: msg.role === 'assistant' ? 'assistant' : 'user',
        content: msg.content
      }))

      const response = await axios.post('http://localhost:8000/query', {
        query: currentQuery,
        conversation_history: conversationHistory
      }, {
        timeout: 60000
      })

      const botMessage = {
        role: 'assistant',
        content: response.data.answer || 'No answer received',
        source: response.data.source_url || ''
      }
      setMessages(prev => [...prev, botMessage])
    } catch (error) {
      console.error('Error:', error)
      
      let errorMsg = 'Failed to get response'
      if (error.response?.data?.detail) {
        if (Array.isArray(error.response.data.detail)) {
          errorMsg = error.response.data.detail.map(e => e.msg).join(', ')
        } else if (typeof error.response.data.detail === 'string') {
          errorMsg = error.response.data.detail
        } else {
          errorMsg = JSON.stringify(error.response.data.detail)
        }
      } else if (error.message) {
        errorMsg = error.message
      }
      
      const errorMessage = {
        role: 'error',
        content: errorMsg
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1>⚡ Arch Assistant</h1>
          <p>Your friendly guide to Arch Linux</p>
        </header>

        <div className="chat-container">
          <div className="messages">
            {messages.length === 0 && (
              <div className="welcome">
                <h2>Hi! I'm your Arch Linux guide 👋</h2>
                <p>I'll help you understand Arch Linux in simple terms. Ask me anything, and I'll break it down step-by-step!</p>
                <div className="examples">
                  <h3>Try asking:</h3>
                  <ul>
                    <li>"How do I install NVIDIA drivers?"</li>
                    <li>"What's the easiest way to update my system?"</li>
                    <li>"Help me set up Bluetooth"</li>
                    <li>"Explain what pacman does"</li>
                  </ul>
                </div>
              </div>
            )}

            {messages.map((msg, idx) => (
              <div key={idx} className={`message ${msg.role}`}>
                {msg.role === 'user' && <div className="avatar">👤</div>}
                {msg.role === 'assistant' && <div className="avatar">⚡</div>}
                {msg.role === 'error' && <div className="avatar">⚠️</div>}
                
                <div className="message-content">
                  {msg.role === 'assistant' ? (
                    <>
                      <ReactMarkdown 
                        remarkPlugins={[remarkGfm]}
                        components={{
                          code({node, inline, className, children, ...props}) {
                            return inline ? (
                              <code className="inline-code" {...props}>
                                {children}
                              </code>
                            ) : (
                              <pre className="code-block">
                                <code className={className} {...props}>
                                  {children}
                                </code>
                              </pre>
                            )
                          }
                        }}
                      >
                        {msg.content}
                      </ReactMarkdown>
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
                <div className="avatar">⚡</div>
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
            <div className="query-row">
              <input
                type="text"
                className="query-input"
                placeholder="Ask me anything about Arch Linux..."
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
