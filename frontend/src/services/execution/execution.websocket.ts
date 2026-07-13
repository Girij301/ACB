import type { ExecutionEvent } from "./types";

export type ExecutionEventHandler = (event: ExecutionEvent) => void;

export class ExecutionWebSocketService {
  private socket: WebSocket | null = null;

  private readonly sessionId: string;

  constructor(sessionId: string) {
    this.sessionId = sessionId;
  }

  connect(
    onEvent: ExecutionEventHandler,
    onOpen?: () => void,
    onClose?: () => void,
    onError?: (event: Event) => void,
  ): void {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      return;
    }

    const apiUrl = import.meta.env.VITE_API_URL;

    const websocketUrl = apiUrl.replace(/^http/, "ws").replace(/\/$/, "");

    this.socket = new WebSocket(`${websocketUrl}/ws/${this.sessionId}`);

    this.socket.onopen = () => {
      onOpen?.();
    };

    this.socket.onmessage = (message) => {
      try {
        const event = JSON.parse(message.data) as ExecutionEvent;

        onEvent(event);
      } catch (error) {
        console.error("Failed to parse execution event.", error);
      }
    };

    this.socket.onerror = (event) => {
      onError?.(event);
    };

    this.socket.onclose = () => {
      onClose?.();

      this.socket = null;
    };
  }

  disconnect(): void {
    this.socket?.close();
    this.socket = null;
  }

  get isConnected(): boolean {
    return this.socket?.readyState === WebSocket.OPEN;
  }
}
