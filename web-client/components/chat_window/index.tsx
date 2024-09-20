"use client";

import React, { useEffect, useState, useCallback, useRef } from 'react';
import { MinusIcon } from '@heroicons/react/24/solid';
import { usePathname } from 'next/navigation';
import Image from 'next/image';
import chatIcon from '@/assets/chatbot.png';
import { CSSTransition } from 'react-transition-group'; // For animation

const hideChatIconPaths = ['/login', '/sign-up'];

export default function ChatWindow() {
  const [messages, setMessages] = useState<{ sender: 'You' | 'Chatbot'; content: string }[]>([]);
  const [input, setInput] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const [isMinimized, setIsMinimized] = useState(true);
  const [isTyping, setIsTyping] = useState(false); // Typing state
  const websocketRef = useRef<WebSocket | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const pathName = usePathname();

  if (hideChatIconPaths.includes(pathName)) {
    return null;
  }

  const connectWebSocket = useCallback(() => {
    const token = localStorage.getItem('token');
    const uri = `ws://localhost:8000/ai/chatbot?token=${token}`;

    const ws = new WebSocket(uri);

    ws.onopen = () => {
      setIsConnected(true);
    };

    ws.onmessage = (event) => {
      const response = JSON.parse(JSON.parse(event.data));
      console.log('Received message:', response);

      if (response.session_id) {
        localStorage.setItem('sessionId', response.session_id);
      }

      if (response.message) {
        setIsTyping(false);
        setMessages((prev) => [...prev, { sender: 'Chatbot', content: response.message }]);
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

    return () => {};
  }, [connectWebSocket]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = useCallback(() => {
    if (input.trim() && websocketRef.current && isConnected) {
      const payload = {
        session_id: localStorage.getItem('sessionId'),
        message: input,
      };
      console.log('Sending payload:', payload);
      websocketRef.current.send(JSON.stringify(payload));
      setMessages((prev) => [...prev, { sender: 'You', content: input }]);
      setInput('');
      setIsTyping(true); 
    }
  }, [input, isConnected]);

  const toggleMinimize = () => {
    setIsMinimized(!isMinimized);
  };

  return (
    <div>
      <div onClick={toggleMinimize} className="fixed bottom-4 right-4 cursor-pointer">
        <Image src={chatIcon} alt="Chat" width={60} height={60} className="rounded-full shadow-lg" />
      </div>
      {!isMinimized && (
        <div
          className={`fixed bottom-0 right-0 m-4 w-80 bg-white shadow-lg rounded-lg overflow-hidden transition-transform ${
            isMinimized ? 'transform translate-y-[calc(100%-2.5rem)]' : ''
          }`}
        >
          <div className="bg-black text-white p-2 flex justify-between items-center">
            <h2 className="font-bold">Customer service</h2>
            <div className="flex space-x-2">
              <button onClick={toggleMinimize} className="text-gray-400 hover:text-gray-200">
                <MinusIcon className="h-5 w-5" />
              </button>
            </div>
          </div>
          <div className="p-4 h-60 overflow-y-auto flex flex-col bg-white custom-scrollbar">
            {messages.length === 0 ? (
              <p className="text-gray-500">No messages yet.</p>
            ) : (
              messages.map((msg, index) => (
                <div
                  key={index}
                  className={`my-2 p-2 rounded flex items-start ${msg.sender === 'You' ? 'justify-end' : 'justify-start'}`}
                >
                  {msg.sender === 'Chatbot' && (
                    <div className="mr-2 flex-shrink-0">
                      <Image src={chatIcon} alt="Chatbot" width={40} height={40} className="rounded-full" />
                    </div>
                  )}
                  <div
                    className={`p-2 rounded max-w-xs ${msg.sender === 'You' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-black'}`}
                  >
                    {msg.content}
                  </div>
                </div>
              ))
            )}
  
            {isTyping && (
              <div className="flex items-start mb-2">
                <div className="mr-2 flex-shrink-0">
                  <Image src={chatIcon} alt="Chatbot typing" width={40} height={40} className="rounded-full" />
                </div>
                <div className="typing-animation bg-gray-200 p-2 rounded flex items-center">
                  <div className="bg-gray-200 w-full p-2 flex justify-center items-center rounded-md">
                    <span className="dot-flashing"></span>
                  </div>
                </div>
              </div>
            )}
  
            <div ref={messagesEndRef} />
          </div>
          <div className="p-4 border-t flex bg-white">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              className="flex-grow border rounded p-2 bg-gray-100 text-black"
              placeholder="Type a message..."
            />
            <button
              onClick={handleSendMessage}
              className={`ml-2 text-white rounded p-2 ${isConnected ? 'bg-blue-500 hover:bg-blue-600' : 'bg-gray-400'}`}
              disabled={!isConnected}
            >
              Send
            </button>
          </div>
        </div>
      )}
    </div>
  );
  
  
}
