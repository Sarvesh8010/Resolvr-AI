import { useEffect, useState } from "react"
import API from "../services/api"

function History() {

  const [history, setHistory] = useState([])

  useEffect(() => {

    fetchHistory()

  }, [])

  const fetchHistory = async () => {

    try {

      const token = localStorage.getItem("token")

      const response = await API.get(
        "/history/",
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )

      setHistory(response.data)

    } catch (error) {

      console.error(error)
    }
  }

  return (
    <div>

      {/* HEADER */}
      <div className="mb-8">

        <h1 className="text-5xl font-bold text-slate-900">
          Chat History
        </h1>

        <p className="text-slate-500 mt-2">
          Previously asked questions and AI responses
        </p>

      </div>

      {/* HISTORY LIST */}
      <div className="space-y-6">

        {history.map((item) => (

          <div
            key={item.id}
            className="bg-white rounded-3xl p-8 shadow-sm border border-slate-200"
          >

            {/* QUESTION */}
            <div className="mb-5">

              <h2 className="text-sm uppercase tracking-wide text-purple-600 font-semibold mb-2">
                Question
              </h2>

              <p className="text-lg font-medium text-slate-900">
                {item.query}
              </p>

            </div>

            {/* ANSWER */}
            <div className="mb-5">

              <h2 className="text-sm uppercase tracking-wide text-purple-600 font-semibold mb-2">
                AI Answer
              </h2>

              <p className="text-slate-700 leading-7 whitespace-pre-line">
                {item.answer}
              </p>

            </div>

            {/* TIMESTAMP */}
            <div className="text-sm text-slate-400">
              {new Date(item.created_at).toLocaleString()}
            </div>

          </div>

        ))}

      </div>

    </div>
  )
}

export default History