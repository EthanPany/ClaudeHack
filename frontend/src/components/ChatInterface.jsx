import React, { useState, useRef, useEffect } from 'react'
import Anthropic from '@anthropic-ai/sdk'
import './ChatInterface.css'

function ChatInterface({ selectedFoods }) {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [recommendation, setRecommendation] = useState(null)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    if (selectedFoods.length > 0 && messages.length === 0) {
      initializeChat()
    }
  }, [selectedFoods])

  const getDiningHallRecommendation = (foods) => {
    const hallCounts = {}
    foods.forEach(food => {
      hallCounts[food.diningHall] = (hallCounts[food.diningHall] || 0) + 1
    })

    const sortedHalls = Object.entries(hallCounts).sort((a, b) => b[1] - a[1])
    return sortedHalls[0] ? sortedHalls[0][0] : null
  }

  const initializeChat = async () => {
    const recommendedHall = getDiningHallRecommendation(selectedFoods)
    setRecommendation(recommendedHall)

    const foodList = selectedFoods.map(f => `${f.name} (${f.diningHall}) - ${f.calories} cal`).join('\n')

    const systemMessage = `You are a helpful dining hall assistant. The user has selected these foods:\n\n${foodList}\n\nBased on their selections, the most frequently appearing dining hall is: ${recommendedHall}. You should recommend this dining hall to them, explain why based on their food preferences, and help them with any questions about dining options. Be friendly, concise, and helpful.`

    setMessages([{
      role: 'assistant',
      content: `Hi! I've analyzed your food selections. Based on what you picked, I recommend visiting **${recommendedHall}**!\n\nThis dining hall has the most items you're interested in. Would you like to know more about the foods there, or do you have any dietary preferences or restrictions I should consider?`
    }])
  }

  const sendMessage = async () => {
    if (!input.trim() || loading) return

    const userMessage = { role: 'user', content: input }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const apiKey = import.meta.env.VITE_ANTHROPIC_API_KEY

      if (!apiKey) {
        throw new Error('Anthropic API key not found. Please add VITE_ANTHROPIC_API_KEY to your .env file.')
      }

      const client = new Anthropic({
        apiKey: apiKey,
        dangerouslyAllowBrowser: true
      })

      const foodList = selectedFoods.map(f => `${f.name} (${f.diningHall}) - ${f.calories} cal`).join('\n')
      const recommendedHall = getDiningHallRecommendation(selectedFoods)

      const systemPrompt = `You are a helpful dining hall assistant. The user has selected these foods:\n\n${foodList}\n\nBased on their selections, the recommended dining hall is: ${recommendedHall}. Help them make dining decisions, answer questions about the food options, and provide helpful recommendations. Be friendly, concise, and informative.`

      const response = await client.messages.create({
        model: 'claude-3-5-sonnet-20241022',
        max_tokens: 1024,
        system: systemPrompt,
        messages: messages.concat(userMessage).map(msg => ({
          role: msg.role,
          content: msg.content
        }))
      })

      const assistantMessage = {
        role: 'assistant',
        content: response.content[0].text
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error('Error calling Claude API:', error)
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `Sorry, I encountered an error: ${error.message}. Please make sure your Anthropic API key is set in the .env file.`
      }])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  if (selectedFoods.length === 0) {
    return (
      <div className="chat-container">
        <div className="empty-state">
          <div className="empty-icon">🍽️</div>
          <h2>No Foods Selected</h2>
          <p>Go back to the Browse Foods page and select some items you like!</p>
          <a href="/" className="back-link">Browse Foods</a>
        </div>
      </div>
    )
  }

  return (
    <div className="chat-container">
      <div className="chat-sidebar">
        <h3 className="sidebar-title">Your Selections</h3>
        {recommendation && (
          <div className="recommendation-badge">
            <span className="badge-label">Recommended Hall</span>
            <span className="badge-value">{recommendation}</span>
          </div>
        )}
        <div className="selected-foods-list">
          {selectedFoods.map(food => (
            <div key={food.id} className="sidebar-food-item">
              <div className="sidebar-food-name">{food.name}</div>
              <div className="sidebar-food-details">
                <span>{food.diningHall}</span>
                <span>{food.calories} cal</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="chat-main">
        <div className="chat-header">
          <h2>AI Dining Assistant</h2>
          <p>Ask me anything about your dining options!</p>
        </div>

        <div className="messages-container">
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.role}`}>
              <div className="message-content">
                {message.content}
              </div>
            </div>
          ))}
          {loading && (
            <div className="message assistant">
              <div className="message-content typing">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="input-container">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask about dietary options, nutrition info, or get more recommendations..."
            className="chat-input"
            rows="2"
            disabled={loading}
          />
          <button
            onClick={sendMessage}
            disabled={!input.trim() || loading}
            className="send-button"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <line x1="22" y1="2" x2="11" y2="13"></line>
              <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
            </svg>
          </button>
        </div>
      </div>
    </div>
  )
}

export default ChatInterface
