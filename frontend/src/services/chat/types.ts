export interface ChatRequest {
  session_id: string;
  message: string;
}

export interface ChatResponse {
  success: boolean;
  message: string;
  data: {
    response: string;
  };
  error: string | null;
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}