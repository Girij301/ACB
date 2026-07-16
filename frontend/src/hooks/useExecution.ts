import { useEffect, useRef } from "react";

import {
  ExecutionService,
  ExecutionWebSocketService,
  type ExecutionEvent,
} from "@/services/execution";

import { useExecutionStore,  useWorkspaceStore, } from "@/store";

export function useExecution() {
  const websocketRef = useRef<ExecutionWebSocketService | null>(null);

  const { state, dispatch, reset, setConnected, setError, setExecution } =
    useExecutionStore();

  const { refreshExplorer } = useWorkspaceStore();

  useEffect(() => {
    return () => {
      websocketRef.current?.disconnect();
      websocketRef.current = null;
    };
  }, []);

  function connect(sessionId: string) {
    if (websocketRef.current) {
      websocketRef.current.disconnect();
    }

    const websocket = new ExecutionWebSocketService(sessionId);

    websocket.connect(
      (event: ExecutionEvent) => {
        console.log(
          "EVENT TYPE:",
          event.type,
          "EXECUTION:",
          event.execution_id,
        );

        dispatch(event);

        if (event.type === "execution_finished") {
          refreshExplorer();

          websocket.disconnect();

          websocketRef.current = null;

          setConnected(false);
        }
      },

      () => {
        setConnected(true);
      },

      () => {
        setConnected(false);
        websocketRef.current = null;
      },

      () => {
        setConnected(false);
        setError("WebSocket connection failed.");
      },
    );

    websocketRef.current = websocket;
  }

  async function execute(
    sessionId: string,
    task: string,
    onStarted?: () => void,
  ) {
    if (state.loading) {
      return;
    }

    reset();

    connect(sessionId);

    onStarted?.();

    setError(null);

    try {
      await ExecutionService.execute({
        session_id: sessionId,
        task,
      });
    } catch (error) {
      console.error(error);

      setError("Failed to execute the plan.");
    }
  }

  return {
    loading: state.loading,
    connected: state.connected,
    error: state.error,
    execution: state.execution,
    steps: state.steps,
    events: state.events,
    activeStep: state.activeStep,
    retryingStep: state.retryingStep,
    debuggingStep: state.debuggingStep,
    validating: state.validating,
    totalSteps: state.totalSteps,
    completedSteps: state.completedSteps,
    successfulSteps: state.successfulSteps,
    failedSteps: state.failedSteps,
    progress: state.progress,
    hasFailed: state.hasFailed,
    currentPhase: state.currentPhase,
    currentAction: state.currentAction,
    timeline: state.timeline,
    execute,
    setExecution,
  };
}
