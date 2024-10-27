import { useState, useEffect, useRef, useCallback } from 'react';
import { v4 as uuidv4 } from 'uuid';

export function useSharedWebSocket() {
  const [isConnected, setIsConnected] = useState(false);
  const [messages, setMessages] = useState<{ sender: "You" | "Chatbot"; content: string }[]>([]);
  const websocketRef = useRef<WebSocket | null>(null);
  const sessionIdRef = useRef<string>(uuidv4());

  const connectWebSocket = useCallback(() => {
    if (websocketRef.current && websocketRef.current.readyState === WebSocket.OPEN) {
      return;
    }

    const token = localStorage.getItem("token");
    const uri = `ws://localhost:8000/ai/chatbot?token=${token}&session_id=${sessionIdRef.current}`;

    const ws = new WebSocket(uri);

    ws.onopen = () => {
      setIsConnected(true);
    };

    ws.onmessage = (event) => {
      const response = JSON.parse(JSON.parse(event.data));
      console.log("Received message:", response);

      if (response.session_id === sessionIdRef.current) {
        if (response.message) {
          setMessages((prev) => [
            ...prev,
            { sender: "Chatbot", content: response.message },
          ]);
        }
      }
    };

    ws.onerror = () => {
      setIsConnected(false);
    };

    ws.onclose = () => {
      setIsConnected(false);
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

  const sendMessage = useCallback((message: string) => {
    if (websocketRef.current && isConnected) {
      const payload = {
        session_id: sessionIdRef.current,
        message: message,
      };
      console.log("Sending payload:", payload);
      websocketRef.current.send(JSON.stringify(payload));
      setMessages((prev) => [...prev, { sender: "You", content: message }]);
    }
  }, [isConnected]);

  return { isConnected, messages, sendMessage, sessionId: sessionIdRef.current };
}
