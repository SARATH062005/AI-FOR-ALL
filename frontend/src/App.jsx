import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './components/Home'
import Login from './components/Login'
import Signup from './components/Signup'
import './App.css'

function App() {
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(localStorage.getItem('token'))

  useEffect(() => {
    if (token) {
      // In a real app, fetch user data here
      // fetch('/users/me', { headers: { Authorization: `Bearer ${token}` } })
    }
  }, [token])

  const login = (newToken) => {
    localStorage.setItem('token', newToken)
    setToken(newToken)
  }

  const logout = () => {
    localStorage.removeItem('token')
    setToken(null)
    setUser(null)
  }

  return (
    <Router>
      <Navbar token={token} logout={logout} />
      <div className="main-content">
        <Routes>
          <Route path="/" element={token ? <Home token={token} /> : <Navigate to="/login" />} />
          <Route path="/login" element={<Login login={login} />} />
          <Route path="/signup" element={<Signup />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
