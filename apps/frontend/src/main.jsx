import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'

import './index.css'

import App from './App.jsx'

import { AuthProvider } from './context/AuthContext'

import { ConversationProvider } from "./context/ConversationContext"

import { Toaster } from "react-hot-toast"

createRoot(document.getElementById('root')).render(
  <StrictMode>

    <ConversationProvider>

      <AuthProvider>

        <App />

        <Toaster
          position="top-right"
          reverseOrder={false}
        />

      </AuthProvider>

    </ConversationProvider>

  </StrictMode>,
)