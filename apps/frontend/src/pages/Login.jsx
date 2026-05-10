import { useState } from "react"
import { useNavigate } from "react-router-dom"

import API from "../services/api"

import { useAuth } from "../context/AuthContext"

function Login() {

  const navigate = useNavigate()

  const { login } = useAuth()

  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")

  const [error, setError] = useState("")

  const handleLogin = async (e) => {

    e.preventDefault()

    setError("")

    try {

      const formData = new URLSearchParams()

      formData.append("username", email)
      formData.append("password", password)

      const response = await API.post(
        "/auth/login",
        formData,
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded"
          }
        }
      )

      login(response.data.access_token)

      navigate("/")

    } catch (err) {

      setError("Invalid credentials")
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center px-6">

      <div className="w-full max-w-md bg-slate-900 border border-slate-800 rounded-3xl p-10">

        <h1 className="text-4xl font-bold text-white mb-2">
          Resolvr AI
        </h1>

        <p className="text-slate-400 mb-8">
          Sign in to continue
        </p>

        <form
          onSubmit={handleLogin}
          className="space-y-5"
        >

          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full px-5 py-4 rounded-2xl bg-slate-800 border border-slate-700 text-white outline-none"
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full px-5 py-4 rounded-2xl bg-slate-800 border border-slate-700 text-white outline-none"
          />

          {error && (
            <p className="text-red-400 text-sm">
              {error}
            </p>
          )}

          <button
            type="submit"
            className="w-full py-4 rounded-2xl bg-purple-600 hover:bg-purple-700 text-white font-semibold transition"
          >
            Sign In
          </button>

        </form>

      </div>

    </div>
  )
}

export default Login