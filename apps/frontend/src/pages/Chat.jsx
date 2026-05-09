import ChatWindow from "../components/ChatWindow"

function Chat() {

  return (
    <div>

      <div className="mb-6">

        <h1 className="text-4xl font-bold text-slate-900">
          AI Chat
        </h1>

        <p className="text-slate-500 mt-2">
          Query uploaded company documents using AI
        </p>

      </div>

      <ChatWindow />

    </div>
  )
}

export default Chat