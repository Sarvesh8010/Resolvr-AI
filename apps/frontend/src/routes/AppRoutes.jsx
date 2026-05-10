import { BrowserRouter, Routes, Route } from "react-router-dom"

import DashboardLayout from "../layouts/DashboardLayout"

import Chat from "../pages/Chat"
import History from "../pages/History"
import Documents from "../pages/Documents"
import Profile from "../pages/Profile"
import Settings from "../pages/Settings"
import Login from "../pages/Login"
import Analytics from "../pages/Analytics"

import ProtectedRoute from "./ProtectedRoute"

function AppRoutes() {

  return (
    <BrowserRouter>

      <Routes>

        <Route
          path="/login"
          element={<Login />}
        />

        <Route
          path="/"
          element={
            <ProtectedRoute>
              <DashboardLayout />
            </ProtectedRoute>
          }
        >

          <Route
            path="chat"
            element={<Chat />}
          />
                  
          <Route
            index
            element={<Chat />}
          />

          <Route
            path="history"
            element={<History />}
          />

          <Route
            path="documents"
            element={<Documents />}
          />

          <Route
            path="profile"
            element={<Profile />}
          />

          <Route
            path="settings"
            element={<Settings />}
          />

          <Route
            path="/analytics"
            element={<Analytics />}
          />

        </Route>

      </Routes>

    </BrowserRouter>
  )
}

export default AppRoutes