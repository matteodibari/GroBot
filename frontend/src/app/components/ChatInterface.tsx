'use client';

/**
 * ChatInterface Component
 * 
 * A clean and simple chat interface built with Next.js and ShadcnUI.
 * Features:
 * - Real-time message display
 * - Auto-scrolling to latest messages
 * - Loading states and error handling
 * - Responsive design
 * - Accessibility support
 * 
 * Uses Zustand for state management and custom hooks for chat functionality.
 */

import React, { useEffect, useRef } from 'react';
import { MessageBubble } from './MessageBubble';
import { InputArea } from './InputArea';
import { useChatStore } from '../store/chatStore';

export const ChatInterface: React.FC = () => {
  // Get chat state and actions from Zustand store
  const { messages, isLoading, error, addMessage } = useChatStore();
  
  // Ref for auto-scrolling to latest messages
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll effect when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="chat-container" role="main" aria-label="Chat Interface">
      {/* Chat Header - Displays the bot name with gradient effect */}
      <div className="chat-header">
        <h2 className="text-2xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
          GroBot
        </h2>
      </div>

      {/* Messages Area - Displays chat history, loading state, and errors */}
      <div className="chat-messages" role="log" aria-live="polite">
        {/* Map through messages and render each in a MessageBubble */}
        {messages.map((message, index) => (
          <MessageBubble 
            key={index} 
            message={message} 
            aria-label={`${message.role} message`}
          />
        ))}
        
        {/* Loading indicator */}
        {isLoading && (
          <div className="flex justify-start mb-4">
            <div className="bg-muted text-foreground rounded-lg px-4 py-2">
              <p className="text-sm" role="status">Thinking...</p>
            </div>
          </div>
        )}
        
        {/* Error display */}
        {error && (
          <div className="flex justify-center mb-4">
            <div className="bg-destructive/10 text-destructive rounded-lg px-4 py-2">
              <p className="text-sm" role="alert">{error}</p>
            </div>
          </div>
        )}
        
        {/* Auto-scroll anchor */}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area - Message input and send button */}
      <InputArea 
        onSendMessage={addMessage} 
        isLoading={isLoading} 
        aria-label="Message input"
      />
    </div>
  );
}; 