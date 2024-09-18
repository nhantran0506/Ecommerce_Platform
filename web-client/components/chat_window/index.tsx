import React, { useEffect, useState, useCallback, useRef } from 'react';
import { useRouter } from 'next/navigation';

export default function ChatWindow() {
  const [messages, setMessages] = useState<string[]>([]);
  const [input, setInput] = useState('');
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const websocketRef = useRef<WebSocket | null>(null);
  const router = useRouter();

  const connectWebSocket = useCallback(() => {
    const token = localStorage.getItem('token');
    const uri = `ws://localhost:8000/ai/chatbot?token=${token}`;

    const ws = new WebSocket(uri);

    ws.onopen = () => {
      console.log("Connected to the chatbot.");
      setIsConnected(true);
    };

    ws.onmessage = (event) => {
      const response = JSON.parse(event.data);
      console.log("Received message:", response);

      if (response.session_id) {
        setSessionId(response.session_id);
        localStorage.setItem('sessionId', response.session_id);
        console.log(`Received session ID: ${response.session_id}`);
      }

      if (response.message) {
        setMessages((prev) => [...prev, `Chatbot: ${response.message}`]);
      }
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
      setIsConnected(false);
    };

    ws.onclose = () => {
      console.log("Disconnected from the chatbot.");
      setIsConnected(false);
      // Attempt to reconnect after a delay
      setTimeout(connectWebSocket, 5000);
    };

    websocketRef.current = ws;
  }, []);

  useEffect(() => {
    connectWebSocket();

    return () => {
      if (websocketRef.current) {
        websocketRef.current.close();
      }
    };
  }, [connectWebSocket]);

  const handleSendMessage = useCallback(() => {
    if (input.trim() && websocketRef.current && isConnected) {
      const payload = {
        session_id: localStorage.getItem('sessionId'),
        message: input,
      };
      console.log("Sending payload:", payload);
      websocketRef.current.send(JSON.stringify(payload));
      setMessages((prev) => [...prev, `You: ${input}`]);
      setInput('');
    } else if (!isConnected) {
      console.log("WebSocket is not connected. Please wait and try again.");
    } else {
      console.log("Cannot send message. Input:", input, "WebSocket:", !!websocketRef.current, "Connected:", isConnected, "SessionId:", sessionId);
    }
  }, [input, isConnected, sessionId]);

  return (
    <div className="fixed bottom-0 right-0 m-4 w-80 bg-white shadow-lg rounded-lg">
      <div className="p-4 border-b">
        <h2 className="font-bold">Chat</h2>
        <p className={`text-sm ${isConnected ? 'text-green-500' : 'text-red-500'}`}>
          {isConnected ? 'Connected' : 'Disconnected'}
        </p>
        <p className="text-sm">Session ID: {sessionId || 'Not set'}</p>
      </div>
      <div className="p-4 h-60 overflow-y-auto">
        {messages.length === 0 ? (
          <p>No messages yet.</p>
        ) : (
          messages.map((msg, index) => (
            <div key={index} className="my-2 p-2 bg-gray-100 rounded">
              {msg}
            </div>
          ))
        )}
      </div>
      <div className="p-4 border-t flex">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="flex-grow border rounded p-2"
          placeholder="Type a message..."
        />
        <button
          onClick={handleSendMessage}
          className={`ml-2 text-white rounded p-2 ${
            isConnected ? 'bg-blue-500' : 'bg-gray-400'
          }`}
          disabled={!isConnected}
        >
          Send
        </button>
      </div>
    </div>
  );
}