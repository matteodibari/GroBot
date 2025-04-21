// Types for chat messages and responses
export interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

export interface ChatRequest {
  messages: Message[];
  temperature?: number;
  max_tokens?: number;
}

export interface ChatResponse {
  response: string;
}

// API client for chat functionality
const API_BASE_URL = 'http://localhost:8000/api';

export async function sendChatMessage(messages: Message[]): Promise<ChatResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        messages,
        temperature: 0.7,
        max_tokens: 500,
      } as ChatRequest),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data as ChatResponse;
  } catch (error) {
    console.error('Error sending chat message:', error);
    throw error;
  }
} 