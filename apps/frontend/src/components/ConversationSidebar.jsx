import { useEffect, useState } from "react"

import { Plus } from "lucide-react"

import API from "../services/api"

import { useConversation } from "../context/ConversationContext"

function ConversationSidebar() {

  const [conversations, setConversations] =
    useState([])

  const { 
    activeConversation,
    setActiveConversation
  } = useConversation()

  // LOAD CONVERSATIONS
  useEffect(() => {

    fetchConversations()

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

  // CREATE NEW CHAT
  const createConversation = async () => {

    try {

      const token = localStorage.getItem("token")

      const response = await API.post(
        "/conversations/?title=New Chat",
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )

      const newConversation = response.data

      setConversations((prev) => [
        newConversation,
        ...prev
      ])

      setActiveConversation(newConversation)

    } catch (error) {

      console.error(error)
    }
  }

  return (
    <div className="w-80 bg-slate-950 border-r border-slate-800 flex flex-col">

      {/* HEADER */}
      <div className="p-5 border-b border-slate-800">

        <button
          onClick={createConversation}
          className="
            w-full
            flex
            items-center
            justify-center
            gap-2
            bg-purple-600
            hover:bg-purple-700
            text-white
            py-3
            rounded-2xl
            transition
          "
        >

          <Plus size={18} />

          New Chat

        </button>

      </div>

      {/* CONVERSATIONS */}
      <div className="flex-1 overflow-y-auto p-3 space-y-2">

        {conversations.map((conversation) => (

          <button
            key={conversation.id}
            onClick={() =>
              setActiveConversation(conversation)
            }
            className={`
              w-full
              text-left
              px-4
              py-3
              rounded-2xl
              transition
              ${
                activeConversation?.id === conversation.id
                  ? "bg-purple-600 text-white"
                  : "hover:bg-slate-800 text-slate-300"
              }
            `}
          >

            <div className="font-medium truncate">
              {conversation.title}
            </div>

          </button>

        ))}

      </div>

    </div>
  )
}

export default ConversationSidebar