import {
  FileText,
  MessageSquare,
  Database
} from "lucide-react"

import {
  useEffect,
  useState
} from "react"

import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip
} from "recharts"

import API from "../services/api"

function Analytics() {

  const [stats, setStats] = useState({
    conversations: 0,
    documents: 0,
    queries: 0
  })

  const [recentQueries, setRecentQueries] =
    useState([])

  useEffect(() => {

    fetchAnalytics()

  }, [])

  const fetchAnalytics = async () => {

    try {

      const token = localStorage.getItem(
        "token"
      )

      const [
        conversationsRes,
        documentsRes,
        historyRes
      ] = await Promise.all([

        API.get("/conversations/", {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }),

        API.get("/documents/", {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }),

        API.get("/history/", {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })

      ])

      setStats({
        conversations:
          conversationsRes.data.length,

        documents:
          documentsRes.data.length,

        queries:
          historyRes.data.length
      })

      setRecentQueries(
        historyRes.data.slice(0, 5)
      )

    } catch (error) {

      console.error(error)
    }
  }

  const cards = [
    {
      title: "Conversations",
      value: stats.conversations,
      icon: MessageSquare
    },
    {
      title: "Documents",
      value: stats.documents,
      icon: FileText
    },
    {
      title: "Queries",
      value: stats.queries,
      icon: Database
    }
  ]

  const chartData = [
    {
      name: "Conversations",
      value: stats.conversations
    },
    {
      name: "Documents",
      value: stats.documents
    },
    {
      name: "Queries",
      value: stats.queries
    }
  ]

  return (
    <div>

      {/* HEADER */}
      <div className="mb-10">

        <h1 className="text-4xl font-bold text-slate-800 mb-3">
          Analytics Dashboard
        </h1>

        <p className="text-slate-500">
          Monitor platform activity and usage
        </p>

      </div>

      {/* STATS */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">

        {cards.map((card, index) => {

          const Icon = card.icon

          return (
            <div
              key={index}
              className="
                bg-white
                rounded-3xl
                p-8
                border
                border-slate-200
                shadow-sm
              "
            >

              <div className="flex items-center justify-between mb-6">

                <div className="text-slate-500 font-medium">
                  {card.title}
                </div>

                <Icon
                  size={28}
                  className="text-purple-500"
                />

              </div>

              <div className="text-5xl font-bold text-slate-800">
                {card.value}
              </div>

            </div>
          )
        })}

      </div>

      {/* DASHBOARD GRID */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

        {/* CHART */}
        <div
          className="
            bg-white
            rounded-3xl
            p-6
            border
            border-slate-200
            shadow-sm
          "
        >

          <h2 className="text-xl font-bold text-slate-800 mb-6">
            Platform Overview
          </h2>

          <div className="h-80">

            <ResponsiveContainer
              width="100%"
              height="100%"
            >

              <BarChart data={chartData}>

                <XAxis dataKey="name" />

                <YAxis />

                <Tooltip />

                <Bar dataKey="value" />

              </BarChart>

            </ResponsiveContainer>

          </div>

        </div>

        {/* RECENT ACTIVITY */}
        <div
          className="
            bg-white
            rounded-3xl
            p-6
            border
            border-slate-200
            shadow-sm
          "
        >

          <h2 className="text-xl font-bold text-slate-800 mb-6">
            Recent Queries
          </h2>

          <div className="space-y-4">

            {recentQueries.map((query) => (

              <div
                key={query.id}
                className="
                  border
                  border-slate-200
                  rounded-2xl
                  p-4
                "
              >

                <div className="font-medium text-slate-800 mb-2">
                  {query.query}
                </div>

                <div className="text-sm text-slate-500">
                  {new Date(
                    query.created_at
                  ).toLocaleString()}
                </div>

              </div>

            ))}

          </div>

        </div>

      </div>

    </div>
  )
}

export default Analytics