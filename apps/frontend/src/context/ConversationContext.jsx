import {
  createContext,
  useContext,
  useState
} from "react"

const ConversationContext = createContext()

export function ConversationProvider({
  children
}) {

  const [
    activeConversation,
    setActiveConversationState
  ] = useState(() => {

    const savedConversation =
      localStorage.getItem(
        "activeConversation"
      )

    return savedConversation
      ? JSON.parse(savedConversation)
      : null
  })

  // PERSIST ACTIVE CONVERSATION
  const setActiveConversation = (
    conversation
  ) => {

    if (conversation) {

      localStorage.setItem(
        "activeConversation",
        JSON.stringify(conversation)
      )

    } else {

      localStorage.removeItem(
        "activeConversation"
      )
    }

    setActiveConversationState(
      conversation
    )
  }

  const [
    messages,
    setMessages
  ] = useState([])

  return (
    <ConversationContext.Provider
      value={{
        activeConversation,
        setActiveConversation,
        messages,
        setMessages
      }}
    >
      {children}
    </ConversationContext.Provider>
  )
}

export function useConversation() {
  return useContext(ConversationContext)
}