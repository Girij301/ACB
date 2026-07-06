import { api } from "@/services/api";

import type {
  ChatRequest,
  ChatResponse,
} from "./types";

export class ChatService {
  static async sendMessage(
    payload: ChatRequest
  ): Promise<ChatResponse> {
    const { data } =
      await api.post<ChatResponse>(
        "/chat",
        payload
      );

    return data;
  }
}