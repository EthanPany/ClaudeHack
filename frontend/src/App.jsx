import React, { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from 'react-router-dom'
import FoodCards from './components/FoodCards'
import ChatInterface from './components/ChatInterface'
import './App.css'

function Navigation() {
  return (
    <nav className="navigation">
      <div className="nav-content">
        <h1 className="nav-title">Dining Hall Guide</h1>
        <div className="nav-links">
          <Link to="/" className="nav-link">Browse Foods</Link>
          <Link to="/chat" className="nav-link">AI Assistant</Link>
        </div>
      </div>
    </nav>
  )
}

function App() {
  const [selectedFoods, setSelectedFoods] = useState([])

  return (
    <Router>
      <div className="app">
        <Navigation />
        <Routes>
          <Route
            path="/"
            element={<FoodCards selectedFoods={selectedFoods} setSelectedFoods={setSelectedFoods} />}
          />
          <Route
            path="/chat"
            element={<ChatInterface selectedFoods={selectedFoods} />}
          />
        </Routes>
      </div>
    </Router>
  )
}

export default App
