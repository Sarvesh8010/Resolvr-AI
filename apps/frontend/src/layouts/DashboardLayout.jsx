import { Outlet, NavLink, useNavigate } from "react-router-dom"

import {
  MessageSquare,
  FileText,
  History,
  User,
  Settings,
  Plus,
  Trash2,
  Pencil
} from "lucide-react"

import { useEffect, useState } from "react"

import API from "../services/api"

import { useConversation } from "../context/ConversationContext"

function DashboardLayout() {

  const navigate = useNavigate()

  const {
    activeConversation,
    setActiveConversation,
    setMessages
  } = useConversation()

  const [conversations, setConversations] =
    useState([])

  const [
    editingConversationId,
    setEditingConversationId
  ] = useState(null)

  const [editingTitle, setEditingTitle] =
    useState("")

  const [searchQuery, setSearchQuery] =
    useState("")

  // LOAD CONVERSATIONS
  useEffect(() => {

    fetchConversations()

    const handleConversationCreated = () => {

      fetchConversations()
    }

    window.addEventListener(
      "conversation-created",
      handleConversationCreated
    )

    return () => {

      window.removeEventListener(
        "conversation-created",
        handleConversationCreated
      )
    }

  }, [])

  const fetchConversations = async () => {

    try {

      const token = localStorage.getItem("token")

      const response = await API.get(
        "/conversations/",
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )

      setConversations(response.data)

    } catch (error) {

      console.error(error)
    }
  }

  // NEW CHAT
  const createConversation = () => {

    setActiveConversation(null)

    setMessages([])

    navigate("/chat")
  }

  const deleteConversation = async (
    conversationId
  ) => {
  
    try {
    
      const token = localStorage.getItem(
        "token"
      )
    
      await API.delete(
        `/conversations/${conversationId}`,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )
    
      setConversations((prev) =>
        prev.filter(
          (conversation) =>
            conversation.id !== conversationId
        )
      )
    
      // CLEAR ACTIVE CHAT
      if (
        activeConversation?.id ===
        conversationId
      ) {
      
        setActiveConversation(null)
      
        setMessages([])
      
        navigate("/chat")
      }
    
    } catch (error) {
    
      console.error(error)
    }
  }

  const renameConversation = async (
    conversationId
  ) => {

    try {

      const token = localStorage.getItem(
        "token"
      )

      await API.put(
        `/conversations/${conversationId}?title=${encodeURIComponent(
          editingTitle
        )}`,
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )

      setConversations((prev) =>
        prev.map((conversation) =>
          conversation.id === conversationId
            ? {
                ...conversation,
                title: editingTitle
              }
            : conversation
        )
      )

      setEditingConversationId(null)

    } catch (error) {

      console.error(error)
    }
  }

  // LOGOUT
  const logout = () => {

    localStorage.removeItem("token")

    localStorage.removeItem("user")

    navigate("/login")
  }

  const navItems = [
    {
      name: "Chat",
      path: "/chat",
      icon: MessageSquare
    },
    {
      name: "Documents",
      path: "/documents",
      icon: FileText
    },
    {
      name: "History",
      path: "/history",
      icon: History
    },
    {
      name: "Profile",
      path: "/profile",
      icon: User
    },
    {
      name: "Settings",
      path: "/settings",
      icon: Settings
    }
  ]

  const user = JSON.parse(
    localStorage.getItem("user")
  )

  const filteredConversations =
    conversations.filter((conversation) =>
      conversation.title
        .toLowerCase()
        .includes(
          searchQuery.toLowerCase()
        )
    )

  return (
    <div className="flex h-screen bg-slate-100">

      {/* SIDEBAR */}
      <div className="w-80 bg-black text-white flex flex-col border-r border-slate-800 h-screen">

        {/* HEADER */}
        <div className="p-6 border-b border-slate-800">

          <h1 className="text-4xl font-bold text-purple-400">
            Resolvr AI
          </h1>

          <p className="text-slate-400 mt-2 text-sm">
            AI-powered document assistant
          </p>

          {/* NEW CHAT */}
          <button
            onClick={createConversation}
            className="
              mt-6
              w-full
              flex
              items-center
              justify-center
              gap-2
              bg-purple-600
              hover:bg-purple-700
              py-3
              rounded-2xl
              transition
            "
          >

            <Plus size={18} />

            New Chat

          </button>

        </div>

        {/* SCROLLABLE SECTION */}
        <div className="flex-1 overflow-y-auto">

          {/* RECENT CHATS */}
          <div className="px-4 pt-5">

            <h3 className="text-xs uppercase tracking-widest text-slate-500 mb-3">
              Recent Chats
            </h3>

            <input
              type="text"
              placeholder="Search conversations..."
              value={searchQuery}
              onChange={(e) =>
                setSearchQuery(e.target.value)
              }
              className="
                w-full
                mb-4
                px-4
                py-3
                rounded-2xl
                bg-slate-900
                border
                border-slate-700
                text-white
                placeholder-slate-400
                outline-none
                focus:border-purple-500
              "
            />

            <div className="space-y-2">

              {filteredConversations.map((conversation) => (
              
                <div
                  key={conversation.id}
                  className="group relative"
                >
                
                  {/* CHAT BUTTON */}
                  <button
                    onClick={() => {
                    
                      if (
                        editingConversationId ===
                        conversation.id
                      ) return
                    
                      setActiveConversation(
                        conversation
                      )
                    
                      navigate("/chat")
                    }}
                    className={`
                      w-full
                      text-left
                      px-4
                      py-3
                      pr-20
                      rounded-2xl
                      transition
                      truncate
                      ${
                        activeConversation?.id ===
                        conversation.id
                          ? "bg-slate-800"
                          : "hover:bg-slate-900"
                      }
                    `}
                  >
                  
                    {editingConversationId ===
                    conversation.id ? (
                    
                      <input
                        value={editingTitle}
                        onChange={(e) =>
                          setEditingTitle(
                            e.target.value
                          )
                        }
                        onKeyDown={(e) => {
                        
                          if (e.key === "Enter") {
                          
                            renameConversation(
                              conversation.id
                            )
                          }
                        
                          if (e.key === "Escape") {
                          
                            setEditingConversationId(
                              null
                            )
                          }
                        }}
                        autoFocus
                        className="
                          bg-transparent
                          outline-none
                          w-full
                          text-white
                        "
                      />
                      
                    ) : (
                    
                      conversation.title
                    
                    )}
            
                  </button>
                  
                  {/* ACTION BUTTONS */}
                  <div
                    className="
                      absolute
                      right-3
                      top-1/2
                      -translate-y-1/2
                      flex
                      items-center
                      gap-2
                      opacity-0
                      group-hover:opacity-100
                      transition
                    "
                  >
                  
                    {/* RENAME */}
                    <button
                      onClick={() => {
                      
                        setEditingConversationId(
                          conversation.id
                        )
                      
                        setEditingTitle(
                          conversation.title
                        )
                      }}
                      className="
                        text-slate-400
                        hover:text-blue-400
                      "
                    >
                    
                      <Pencil size={15} />
                    
                    </button>
                    
                    {/* DELETE */}
                    <button
                      onClick={() =>
                        deleteConversation(
                          conversation.id
                        )
                      }
                      className="
                        text-slate-400
                        hover:text-red-400
                      "
                    >
                    
                      <Trash2 size={15} />
                    
                    </button>
                    
                  </div>
                    
                </div>
            
              ))}
            
            </div>

          </div>

          {/* NAVIGATION */}
          <div className="px-4 pt-8 pb-8">

            <h3 className="text-xs uppercase tracking-widest text-slate-500 mb-3">
              Navigation
            </h3>

            <nav className="space-y-2">

              {navItems.map((item) => {

                const Icon = item.icon

                return (
                  <NavLink
                    key={item.name}
                    to={item.path}
                    className={({ isActive }) =>
                      `
                      flex items-center gap-3 px-4 py-3 rounded-2xl transition
                      ${
                        isActive
                          ? "bg-purple-600 text-white"
                          : "hover:bg-slate-900 text-slate-300"
                      }
                      `
                    }
                  >

                    <Icon size={20} />

                    {item.name}

                  </NavLink>
                )
              })}

            </nav>

          </div>

        </div>

        {/* USER */}
        <div className="p-4 border-t border-slate-800">

          <div className="bg-slate-900 rounded-3xl p-4">

            <div className="font-semibold">
              {user?.email}
            </div>

            <div className="text-sm text-slate-400 mt-1">
              {user?.role}
            </div>

            <button
              onClick={logout}
              className="
                mt-4
                w-full
                bg-red-500
                hover:bg-red-600
                py-3
                rounded-2xl
                transition
              "
            >
              Logout
            </button>

          </div>

        </div>

      </div>

      {/* MAIN CONTENT */}
      <div className="flex-1 overflow-y-auto p-8">

        <Outlet />

      </div>

    </div>
  )
}

export default DashboardLayout