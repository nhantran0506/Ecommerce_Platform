"use client";

import React, { useEffect, useState, useCallback, useRef } from "react";
import { Minus } from "react-feather";
import { usePathname, useRouter } from "next/navigation";
import Image from "next/image";
import chatIcon from "@/assets/chatbot.png";
import { API_BASE_URL, API_ROUTES } from "@/libraries/api";
import { BotIcon } from "lucide-react";

const hideChatIconPaths = ["/login", "/sign-up"];

export default function ChatWindow() {
  const [messages, setMessages] = useState<{ sender: "You" | "Chatbot"; content: string }[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isMinimized, setIsMinimized] = useState(true);
  const [isTyping, setIsTyping] = useState(false);
  const [fullUrl, setFullUrl] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const pathName = usePathname();
  const router = useRouter();
  const isInitialMount = useRef(true);

  // Load initial state from localStorage
  useEffect(() => {
    if (isInitialMount.current) {
      const storedMessages = localStorage.getItem("chatMessages");
      const storedMinimizedState = localStorage.getItem("chatMinimized");
      
      if (storedMessages) {
        setMessages(JSON.parse(storedMessages));
      }
      
      if (storedMinimizedState !== null) {
        setIsMinimized(JSON.parse(storedMinimizedState));
      }

      isInitialMount.current = false;
    }
  }, []);

  // Save messages to localStorage
  useEffect(() => {
    if (!isInitialMount.current) {
      localStorage.setItem("chatMessages", JSON.stringify(messages));
    }
  }, [messages]);

  // Save minimized state to localStorage
  useEffect(() => {
    if (!isInitialMount.current) {
      localStorage.setItem("chatMinimized", JSON.stringify(isMinimized));
    }
  }, [isMinimized]);

  // Handle search navigation
  const handleSearch = useCallback((searchQuery: string) => {
    const url = `/products?search=${encodeURIComponent(searchQuery)}`;
    router.push(url);
  }, [router]);

  const handleSendMessage = useCallback(async () => {
    if (input.trim() && !isLoading) {
      try {
        setIsLoading(true);
        setIsTyping(true);

        setMessages((prev) => [...prev, { sender: "You", content: input }]);
        setInput("");

        const sessionId = localStorage.getItem("sessionId") || " ";

        const payload = {
          model: "llama3.2",
          session_id: sessionId,
          query: input,
          current_route:`${fullUrl}` ,
        };

        const response = await fetch(
          `${API_BASE_URL}${API_ROUTES.CHAT_MESSAGE}`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
            body: JSON.stringify(payload),
          }
        );

        if (!response.ok) {
          throw new Error("Failed to send message");
        }

        const data = await response.json();

        if (data.session_id) {
          localStorage.setItem("sessionId", data.session_id);
        }

        // Always add the bot's response to messages
        if (data.response) {
          setMessages((prev) => [
            ...prev,
            { sender: "Chatbot", content: data.response },
          ]);
        }

        // Handle search navigation after adding the message
        if (data.purpose === "search") {
          handleSearch(data.response);
        }

      } catch (error) {
        console.error("Error sending message:", error);
        setMessages((prev) => [
          ...prev,
          {
            sender: "Chatbot",
            content: "The service is not available right now, please try later.",
          },
        ]);
      } finally {
        setIsTyping(false);
        setIsLoading(false);
      }
    }
  }, [input, isLoading, fullUrl, handleSearch]);

  const toggleMinimize = () => {
    setIsMinimized(!isMinimized);
  };

  if (hideChatIconPaths.includes(pathName)) {
    return null;
  }

  return (
    <div>
      <div
        onClick={toggleMinimize}
        className="fixed bottom-4 right-4 cursor-pointer rounded-full shadow-md bg-black p-2"
      >
        <BotIcon size={40} color="white" />
      </div>
      {!isMinimized && (
        <div
          className={`fixed bottom-0 right-0 m-4 w-96 bg-white shadow-lg rounded-lg overflow-hidden transition-transform z-50 ${
            isMinimized ? "transform translate-y-[calc(100%-2.5rem)]" : ""
          }`}
        >
          <div className="bg-black text-white p-3 flex justify-between items-center">
            <h2 className="font-bold text-lg">Customer service</h2>
            <div className="flex space-x-2">
              <button
                onClick={toggleMinimize}
                className="text-gray-400 hover:text-gray-200"
              >
                <Minus className="h-6 w-6" />
              </button>
            </div>
          </div>
          <div className="p-4 h-96 overflow-y-auto flex flex-col bg-white custom-scrollbar">
            {messages.length === 0 ? (
              <p className="text-gray-500">No messages yet.</p>
            ) : (
              messages.map((msg, index) => (
                <div
                  key={index}
                  className={`my-2 p-2 rounded flex items-start ${
                    msg.sender === "You" ? "justify-end" : "justify-start"
                  }`}
                >
                  {msg.sender === "Chatbot" && (
                    <div className="mr-2 flex-shrink-0">
                      <Image
                        src={chatIcon}
                        alt="Chatbot"
                        width={40}
                        height={40}
                        className="rounded-full"
                      />
                    </div>
                  )}
                  <div
                    className={`p-2 rounded max-w-xs ${
                      msg.sender === "You"
                        ? "bg-blue-600 text-white"
                        : "bg-gray-200 text-black"
                    }`}
                  >
                    {msg.content}
                  </div>
                </div>
              ))
            )}

            {isTyping && (
              <div className="flex items-start mb-2">
                <div className="mr-2 flex-shrink-0">
                  <Image
                    src={chatIcon}
                    alt="Chatbot typing"
                    width={40}
                    height={40}
                    className="rounded-full"
                  />
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
              onKeyPress={(e) => {
                if (e.key === "Enter") {
                  handleSendMessage();
                }
              }}
              className="flex-grow border rounded p-3 bg-gray-100 text-black text-base"
              placeholder="Type a message..."
            />
            <button
              onClick={handleSendMessage}
              className={`ml-3 text-white rounded px-6 py-3 text-base ${
                !isLoading ? "bg-blue-500 hover:bg-blue-600" : "bg-gray-400"
              }`}
              disabled={isLoading}
            >
              Send
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
