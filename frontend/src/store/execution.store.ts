import { create } from "zustand";

import {
  executionReducer,
  initialExecutionState,
  type ExecutionState,
} from "@/services/execution";

import type { ExecutionEvent } from "@/services/execution";

interface ExecutionStore {
  state: ExecutionState;

  setState: (state: ExecutionState) => void;

  dispatch: (event: ExecutionEvent) => void;

  setConnected: (connected: boolean) => void;

  setError: (error: string | null) => void;

  setExecution: (
    execution: ExecutionState["execution"],
  ) => void;

  reset: () => void;
}

export const useExecutionStore =
  create<ExecutionStore>((set, get) => ({
    state: initialExecutionState,

    setState: (state) =>
      set({
        state,
      }),

    dispatch: (event) =>
      set({
        state: executionReducer(
          get().state,
          event,
        ),
      }),

    setConnected: (connected) =>
      set((store) => ({
        state: {
          ...store.state,
          connected,
        },
      })),

    setError: (error) =>
      set((store) => ({
        state: {
          ...store.state,
          error,
        },
      })),

    setExecution: (execution) =>
      set((store) => ({
        state: {
          ...store.state,
          execution,
        },
      })),

    reset: () =>
      set({
        state: initialExecutionState,
      }),
  }));