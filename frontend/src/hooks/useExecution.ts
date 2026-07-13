import { useEffect, useRef } from "react";

import {
  ExecutionService,
  ExecutionWebSocketService,
  type ExecutionEvent,
} from "@/services/execution";

import { useExecutionStore } from "@/store";

export function useExecution() {
  const websocketRef =
    useRef<ExecutionWebSocketService | null>(null);

  const {
    loading,
    connected,
    error,
    execution,
    steps,
    events,

    setLoading,
    setConnected,
    setError,
    setExecution,
    setSteps,
    addEvent,
    clear,
  } = useExecutionStore();

  useEffect(() => {
    return () => {
      websocketRef.current?.disconnect();
    };
  }, []);

  function connect(sessionId: string) {
    if (
      websocketRef.current?.isConnected
    ) {
      return;
    }

    const websocket =
      new ExecutionWebSocketService(sessionId);

    websocket.connect(
      (event: ExecutionEvent) => {
        addEvent(event);

        switch (event.type) {
          case "execution_started":
            setLoading(true);
            break;

          case "execution_finished":
            setLoading(false);
            break;

          default:
            break;
        }
      },

      () => {
        setConnected(true);
      },

      () => {
        setConnected(false);
      },

      () => {
        setError("WebSocket connection failed.");
      },
    );

    websocketRef.current = websocket;
  }

  async function execute(
    sessionId: string,
    task: string,
  ) {
    if (loading) {
      return;
    }

    clear();

    connect(sessionId);

    setLoading(true);

    setError(null);

    try {
      await ExecutionService.execute({
        session_id: sessionId,
        task,
      });

      /**
       * Everything after this point
       * is driven by WebSocket events.
       */
    } catch (error) {
      console.error(error);

      setLoading(false);

      setError(
        "Failed to execute the plan.",
      );
    }
  }

  return {
    loading,

    connected,

    error,

    execution,

    steps,

    events,

    execute,

    setExecution,

    setSteps,
  };
}