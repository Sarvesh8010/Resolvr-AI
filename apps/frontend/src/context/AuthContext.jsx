import { createContext, useContext, useEffect, useState } from "react"

import API from "../services/api"

const AuthContext = createContext()

export function AuthProvider({ children }) {

  const [token, setToken] = useState(
    localStorage.getItem("token")
  )

  const [user, setUser] = useState(null)

  // FETCH CURRENT USER
  const fetchUser = async () => {

    try {

      const storedToken = localStorage.getItem("token")

      if (!storedToken) return

      const response = await API.get(
        "/auth/me",
        {
          headers: {
            Authorization: `Bearer ${storedToken}`
          }
        }
      )

      setUser(response.data)

    } catch (error) {

      console.error(error)

      logout()
    }
  }

  useEffect(() => {

    if (token) {
      fetchUser()
    }

  }, [token])

  // LOGIN
  const login = (newToken) => {

    localStorage.setItem(
      "token",
      newToken
    )

    setToken(newToken)
  }

  // LOGOUT
  const logout = () => {

    localStorage.removeItem("token")

    setToken(null)

    setUser(null)
  }

  return (
    <AuthContext.Provider
      value={{
        token,
        user,
        login,
        logout,
        isAuthenticated: !!token
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}