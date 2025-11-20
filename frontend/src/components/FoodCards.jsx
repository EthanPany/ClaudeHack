import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import './FoodCards.css'

function FoodCards({ selectedFoods, setSelectedFoods }) {
  const [foods, setFoods] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const navigate = useNavigate()

  useEffect(() => {
    fetchFoods()
  }, [])

  const fetchFoods = async () => {
    try {
      const response = await fetch('/api/foods')
      if (!response.ok) {
        throw new Error('Failed to fetch foods')
      }
      const data = await response.json()
      setFoods(data)
      setLoading(false)
    } catch (err) {
      setError(err.message)
      setLoading(false)
    }
  }

  const toggleFoodSelection = (food) => {
    setSelectedFoods(prev => {
      const isSelected = prev.some(f => f.id === food.id)
      if (isSelected) {
        return prev.filter(f => f.id !== food.id)
      } else {
        return [...prev, food]
      }
    })
  }

  const isFoodSelected = (foodId) => {
    return selectedFoods.some(f => f.id === foodId)
  }

  const goToChatWithSelections = () => {
    if (selectedFoods.length > 0) {
      navigate('/chat')
    }
  }

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p>Loading delicious foods...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="error-container">
        <h2>Oops! Something went wrong</h2>
        <p>{error}</p>
        <button onClick={fetchFoods} className="retry-button">Try Again</button>
      </div>
    )
  }

  return (
    <div className="food-cards-container">
      <div className="header-section">
        <h2 className="page-title">Explore Dining Halls</h2>
        <p className="page-subtitle">Select foods you like and get AI recommendations!</p>
        {selectedFoods.length > 0 && (
          <div className="selection-banner">
            <span>{selectedFoods.length} item{selectedFoods.length !== 1 ? 's' : ''} selected</span>
            <button onClick={goToChatWithSelections} className="chat-button">
              Get AI Recommendations
            </button>
          </div>
        )}
      </div>

      <div className="cards-grid">
        {foods.map(food => (
          <div
            key={food.id}
            className={`food-card ${isFoodSelected(food.id) ? 'selected' : ''}`}
            onClick={() => toggleFoodSelection(food)}
          >
            <div className="card-image-container">
              {food.image_url ? (
                <img
                  src={food.image_url}
                  alt={food.name}
                  className="card-image"
                  loading="lazy"
                />
              ) : (
                <div className="placeholder-image">No Image</div>
              )}
              {isFoodSelected(food.id) && (
                <div className="selected-checkmark">✓</div>
              )}
            </div>
            <div className="card-content">
              <h3 className="food-name">{food.name}</h3>
              <div className="food-details">
                <span className="dining-hall">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                    <polyline points="9 22 9 12 15 12 15 22"></polyline>
                  </svg>
                  {food.diningHall}
                </span>
                <span className="calories">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
                    <path d="M2 17l10 5 10-5"></path>
                    <path d="M2 12l10 5 10-5"></path>
                  </svg>
                  {food.calories} cal
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default FoodCards
