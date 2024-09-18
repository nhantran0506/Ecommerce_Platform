'use client';

import React, { useState } from 'react';
import Image from 'next/image';
import chatIcon from '@/assets/chat-icon.png';
import ChatWindow from '../chat_window';

const ChatIcon: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleChatWindow = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div>
      <div 
        onClick={toggleChatWindow} 
        className="fixed bottom-4 right-4 cursor-pointer"
      >
        <Image 
          src={chatIcon} 
          alt="Chat" 
          width={60} 
          height={60} 
          className="rounded-full shadow-lg"
        />
      </div>
      {isOpen && <ChatWindow />}
    </div>
  );
};

export default ChatIcon;

