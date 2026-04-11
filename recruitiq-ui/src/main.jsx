import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import ParticleBackground from './ParticleBackground'
import Navbar from './Navbar'
import Home from './Home'
import './index.css'
import './App.css'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <ParticleBackground />
    <Navbar />
    <Home />
  </StrictMode>,
)
