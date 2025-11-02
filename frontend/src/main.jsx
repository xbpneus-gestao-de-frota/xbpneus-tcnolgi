import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App'
import './index.css'
import { setupTokenRefreshInterval } from './api/auth'

// Configurar renovação automática de token ao iniciar a aplicação
setupTokenRefreshInterval()

ReactDOM.createRoot(document.getElementById('root')).render(
  <BrowserRouter>
    <App />
  </BrowserRouter>
)

