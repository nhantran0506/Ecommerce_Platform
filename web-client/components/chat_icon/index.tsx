'use client';

import React, { useState } from 'react';
import Image from 'next/image';
import { usePathname } from 'next/navigation';
import chatIcon from '@/assets/chat-icon.png';
import ChatWindow from '../chat_window';

const ChatIcon: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const pathname = usePathname();

  const hideChatIconPaths = ['/login', '/sign-up'];

  const toggleChatWindow = () => {
    setIsOpen(!isOpen);
  };

  if (hideChatIconPaths.includes(pathname)) {
    return null;
  }

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
      {isOpen && <ChatWindow onClose={() => setIsOpen(false)} />}
    </div>
  );
};

export default ChatIcon;