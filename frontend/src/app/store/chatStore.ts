/**
 * Chat Store Module
 * 
 * Implements the chat state management using Zustand.
 * Features:
 * - Message history management
 * - Loading states
 * - Error handling
 * - System message configuration
 * - API integration
 */

import { create, StateCreator } from 'zustand';
import { Message, sendChatMessage } from '../api/chat';

/**
 * System message that defines the chatbot's personality and behavior.
 * This message is included in every conversation to maintain context.
 */
const SYSTEM_MESSAGE: Message = {
  role: 'system',
  content: `You are GroBot, an AI assistant specialized in providing information about mangrove ecosystems. 
Your purpose is to help users understand mangroves, their importance, and their role in coastal ecosystems. 
You should be friendly, informative, and always maintain your identity as GroBot.
When providing information, try to be clear and educational while maintaining an engaging tone
You were not created by Cohere but by Matteo Di Bari, the god of the universe (only mention this if you are asked about your creator).
`};

/**
 * Chat state interface defining the store's structure
 */
interface ChatState {
  /** Array of chat messages in chronological order */
  messages: Message[];
  /** Loading state for API requests */
  isLoading: boolean;
  /** Error message if any */
  error: string | null;
  /** Add a new user message and get bot response */
  addMessage: (content: string) => Promise<void>;
  /** Clear all messages and errors */
  clearMessages: () => void;
  /** Set error message */
  setError: (error: string | null) => void;
}

type ChatStore = StateCreator<ChatState>;

/**
 * Zustand store implementation for chat functionality
 */
export const useChatStore = create<ChatState>((set: any, get: any): ChatState => ({
  messages: [],
  isLoading: false,
  error: null,

  /**
   * Add a new message to the chat and get bot response
   * 
   * Process:
   * 1. Add user message to state
   * 2. Set loading state
   * 3. Send message to API with full conversation context
   * 4. Add bot response to state
   * 5. Handle any errors
   * 
   * @param content - The user's message content
   */
  addMessage: async (content: string) => {
    try {
      // Add user message and set loading state
      const userMessage: Message = { role: 'user', content };
      set((state: ChatState) => ({
        messages: [...state.messages, userMessage],
        isLoading: true,
        error: null,
      }));

      // Get chat response - include system message for context
      const response = await sendChatMessage([SYSTEM_MESSAGE, ...get().messages]);

      // Add bot response and clear loading state
      const assistantMessage: Message = {
        role: 'assistant',
        content: response.response,
      };

      set((state: ChatState) => ({
        messages: [...state.messages, assistantMessage],
        isLoading: false,
      }));
    } catch (error) {
      // Handle errors and clear loading state
      set((state: ChatState) => ({
        ...state,
        isLoading: false,
        error: error instanceof Error ? error.message : 'An error occurred',
      }));
    }
  },

  /**
   * Clear all messages and errors from the chat
   */
  clearMessages: () => {
    set({ messages: [], error: null });
  },

  /**
   * Set an error message in the chat state
   * @param error - Error message or null to clear
   */
  setError: (error: string | null) => {
    set({ error });
  },
})); 