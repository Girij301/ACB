import type { ExecutionEvent } from "./types";

export type ExecutionEventHandler = (event: ExecutionEvent) => void;

export class ExecutionWebSocketService {
  private socket: WebSocket | null = null;

  private readonly sessionId: string;

  constructor(sessionId: string) {
    this.sessionId = sessionId;
  }

  private cleanup(): void {
    if (!this.socket) {
      return;
    }

    this.socket.onopen = null;
    this.socket.onmessage = null;
    this.socket.onerror = null;
    this.socket.onclose = null;

    this.socket.close();

    this.socket = null;
  }

  connect(
    onEvent: ExecutionEventHandler,
    onOpen?: () => void,
    onClose?: () => void,
    onError?: (event: Event) => void,
  ): void {
    if (this.socket?.readyState === WebSocket.OPEN) {
      return;
    }

    this.cleanup();

    const websocketUrl = import.meta.env.VITE_WS_URL;

    this.socket = new WebSocket(
      `${websocketUrl}/ws/${this.sessionId}`,
    );

    this.socket.onopen = () => {
      onOpen?.();
    };

    this.socket.onmessage = (message) => {
      if (!message.data) {
        return;
      }

      try {
        const event = JSON.parse(message.data) as ExecutionEvent;

        onEvent(event);
      } catch (error) {
        console.warn("Ignoring malformed execution event.", error);
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
    this.cleanup();
  }

  get isConnected(): boolean {
    return this.socket?.readyState === WebSocket.OPEN;
  }
}
