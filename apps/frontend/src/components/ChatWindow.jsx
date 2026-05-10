import { useEffect, useRef, useState } from "react"

import { Send } from "lucide-react"

import { motion } from "framer-motion"

import ReactMarkdown from "react-markdown"

import API from "../services/api"

import { useConversation } from "../context/ConversationContext"

function ChatWindow() {

  const {
    activeConversation,
    setActiveConversation,
    messages,
    setMessages
  } = useConversation()

  const [input, setInput] = useState("")

  const [loading, setLoading] = useState(false)

  const messagesEndRef = useRef(null)

  // AUTO SCROLL
  useEffect(() => {

    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth"
    })

  }, [messages])

  // LOAD CONVERSATION MESSAGES
  useEffect(() => {

    if (!activeConversation) {

      setMessages([])

      return
    }

    loadConversationMessages()

  }, [activeConversation])

  const loadConversationMessages = async () => {

    const skipLoad = localStorage.getItem(
      "skip_next_load"
    )

    if (skipLoad === "true") {

      localStorage.removeItem(
        "skip_next_load"
      )

      return
    }
  
    try {
    
      const token = localStorage.getItem("token")
    
      const response = await API.get(
        `/conversations/${activeConversation.id}`,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )
    
      const formattedMessages = []

      // SAFETY CHECK
      if (Array.isArray(response.data)) {
    
        response.data.forEach((msg) => {
      
          formattedMessages.push({
            role: "user",
            content: msg.query
          })
      
          formattedMessages.push({
            role: "ai",
            content: msg.answer
          })
      
        })

      }
    
      setMessages(formattedMessages)
    
    } catch (error) {
    
      console.error(error)

      setMessages([])
    } 
  }


  // SEND MESSAGE
  const sendMessage = async () => {

    if (!input.trim()) return

    const question = input
      
    setInput("")
      
    // AUTO CREATE CONVERSATION
    let currentConversation = activeConversation
      
    if (!currentConversation) {
    
      try {
      
        const token = localStorage.getItem("token")
      
        const createResponse = await API.post(
          `/conversations/?title=${encodeURIComponent(
            question.slice(0, 40)
          )}`,
          {},
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        )
      
        currentConversation = createResponse.data
      
        setActiveConversation(currentConversation)

        localStorage.setItem(
        "skip_next_load",
        "true"
        )
      
        // REFRESH SIDEBAR
        window.dispatchEvent(
          new Event("conversation-created")
        )
      
      } catch (error) {
      
        console.error(error)
      
        alert("Failed to create conversation")
      
        return
      }
    }
    
    // ADD USER MESSAGE AFTER CONVERSATION EXISTS
    const userMessage = {
      role: "user",
      content: question
    }
    
    setMessages((prev) => [
      ...prev,
      userMessage
    ])

    setLoading(true)

    // TEMP AI MESSAGE
    const aiMessage = {
      role: "ai",
      content: "",
      sources: []
    }

    setMessages((prev) => [
      ...prev,
      aiMessage
    ])

    try {

      const token = localStorage.getItem("token")

      const response = await fetch(
        `http://127.0.0.1:8000/query/stream?q=${encodeURIComponent(question)}&conversation_id=${currentConversation.id}`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )

      const reader = response.body.getReader()

      const decoder = new TextDecoder()

      let streamedText = ""

      while (true) {

        const { done, value } = await reader.read()

        if (done) break

        const chunk = decoder.decode(value)

        streamedText += chunk

        setMessages((prev) => {

          const updated = [...prev]

          updated[updated.length - 1] = {
            ...updated[updated.length - 1],
            content: streamedText
          }

          return updated
        })
      }

    } catch (error) {

      console.error(error)

      setMessages((prev) => {

        const updated = [...prev]

        updated[updated.length - 1] = {
          role: "ai",
          content: "❌ Error streaming response."
        }

        return updated
      })
    }

    setLoading(false)
  }

  return (
    <div className="flex flex-col h-[82vh] bg-white rounded-3xl shadow-sm overflow-hidden border border-slate-200">

      {/* CHAT AREA */}
      <div className="flex-1 overflow-y-auto p-8 space-y-8 bg-slate-50">

        {messages?.length === 0 && (

          <div className="h-full flex flex-col items-center justify-center">
          
            <div className="text-center mb-10">

              <h2 className="text-5xl font-bold text-slate-800 mb-4">
                Resolvr AI
              </h2>

              <p className="text-slate-500 text-lg">
                Ask questions about your uploaded documents
              </p>

            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 w-full max-w-3xl">

              {[
                "Summarize uploaded documents",
                "Explain the refund policy",
                "What is the shipping process?",
                "Give insights from uploaded files"
              ].map((prompt, index) => (
              
                <button
                  key={index}
                  onClick={() => {
                  
                    setInput(prompt)
                    setTimeout(() => {
                      sendMessage()
                    }, 100)
                  }}
                  className="
                    bg-white
                    border
                    border-slate-200
                    hover:border-purple-400
                    hover:shadow-md
                    rounded-3xl
                    p-6
                    text-left
                    transition
                  "
                >
                
                  <div className="font-semibold text-slate-800 mb-2">
                    {prompt}
                  </div>
                
                  <div className="text-sm text-slate-500">
                    Click to use this prompt
                  </div>
                
                </button>

              ))}

            </div>
            
          </div>
        )}

        {messages?.map((msg, index) => (

          <motion.div
            key={index}
            initial={{
              opacity: 0,
              y: 10
            }}
            animate={{
              opacity: 1,
              y: 0
            }}
            transition={{
              duration: 0.25
            }}
            className={`flex ${
              msg.role === "user"
                ? "justify-end"
                : "justify-start"
            }`}
          >

            <div
              className={`max-w-4xl px-6 py-5 rounded-3xl shadow-sm ${
                msg.role === "user"
                  ? "bg-purple-600 text-white"
                  : "bg-white border border-slate-200"
              }`}
            >

              {/* MARKDOWN CONTENT */}
              <div className="prose prose-slate max-w-none">

                <ReactMarkdown>
                  {msg.content}
                </ReactMarkdown>

              </div>

              {/* SOURCES */}
              {msg.sources?.length > 0 && (
              
                <div className="mt-6 space-y-3">
                
                  <h4 className="text-sm font-semibold text-slate-500 uppercase tracking-wide">
                    Sources
                  </h4>
              
                  {msg.sources.map((source, idx) => (
                  
                    <details
                      key={idx}
                      className="
                        bg-slate-100
                        border
                        border-slate-200
                        rounded-2xl
                        overflow-hidden
                        group
                      "
                    >
                    
                      <summary
                        className="
                          list-none
                          cursor-pointer
                          px-5
                          py-4
                          flex
                          items-center
                          justify-between
                          hover:bg-slate-200
                          transition
                        "
                      >
                      
                        <div>
                  
                          <div className="font-semibold text-slate-800">
                            📄 {source.source}
                          </div>
                  
                          <div className="text-sm text-slate-500 mt-1">
                            Click to expand source
                          </div>
                  
                        </div>
                  
                        <div className="text-slate-400 group-open:rotate-180 transition">
                          ▼
                        </div>
                  
                      </summary>
                  
                      <div className="px-5 pb-5">
                  
                        <div
                          className="
                            bg-white
                            border
                            border-slate-200
                            rounded-2xl
                            p-4
                            text-sm
                            text-slate-700
                            leading-7
                            whitespace-pre-wrap
                          "
                        >
                        
                          {source.text}
                  
                        </div>
                  
                      </div>
                  
                    </details>
              
                  ))}
              
                </div>
              
              )}

            </div>

          </motion.div>

        ))}

        {/* TYPING */}
        {loading && (

          <motion.div
            initial={{
              opacity: 0
            }}
            animate={{
              opacity: 1
            }}
            className="flex"
          >

            <div className="bg-white border border-slate-200 px-6 py-5 rounded-3xl shadow-sm">

              <div className="flex gap-2">

                <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"></div>

                <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce delay-100"></div>

                <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce delay-200"></div>

              </div>

            </div>

          </motion.div>

        )}

        <div ref={messagesEndRef}></div>

      </div>

      {/* INPUT AREA */}
      <div className="border-t border-slate-200 bg-white p-5">

        <div className="flex items-center gap-4">

          <input
            type="text"
            placeholder="Ask something about your documents..."
            value={input}
            onChange={(e) =>
              setInput(e.target.value)
            }
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                sendMessage()
              }
            }}
            className="
              flex-1
              px-6
              py-4
              rounded-2xl
              border
              border-slate-300
              outline-none
              focus:ring-2
              focus:ring-purple-500
              text-slate-700
            "
          />

          <button
            onClick={sendMessage}
            disabled={loading}
            className="
              bg-purple-600
              hover:bg-purple-700
              disabled:opacity-50
              text-white
              p-4
              rounded-2xl
              transition
            "
          >
            <Send size={22} />
          </button>

        </div>

      </div>

    </div>
  )
}

export default ChatWindow