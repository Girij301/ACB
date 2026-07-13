import { create } from "zustand";

interface ChatState {
  sessionId: string;

  setSessionId: (
    sessionId: string,
  ) => void;
}

export const useChatStore =
  create<ChatState>((set) => ({
    sessionId: crypto.randomUUID(),

    setSessionId: (sessionId) =>
      set({
        sessionId,
      }),
  }));