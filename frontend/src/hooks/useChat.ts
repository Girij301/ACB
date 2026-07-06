import { useState } from "react";

import {
  ChatService,
  type ChatMessage,
} from "@/services/chat";

export function useChat(
  sessionId: string,
) {
  const [messages, setMessages] = useState<
    ChatMessage[]
  >([]);

  const [loading, setLoading] =
    useState(false);

  async function sendMessage(
    content: string,
  ) {
    if (!content.trim()) return;

    const userMessage: ChatMessage = {
      role: "user",
      content,
    };

    setMessages((previous) => [
      ...previous,
      userMessage,
    ]);

    setLoading(true);

    try {
      const response =
        await ChatService.sendMessage({
          session_id: sessionId,
          message: content,
        });

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content:
            response.data.response,
        },
      ]);
    } catch (error) {
      console.error(error);

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content:
            "Something went wrong while contacting the AI.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return {
    messages,
    loading,
    sendMessage,
  };
}