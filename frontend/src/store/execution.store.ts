import { create } from "zustand";

import type {
  ExecutionEvent,
  ExecutionSummary,
  StepResult,
} from "@/services/execution";

interface ExecutionState {
  loading: boolean;

  connected: boolean;

  error: string | null;

  execution: ExecutionSummary | null;

  steps: StepResult[];

  events: ExecutionEvent[];

  setLoading: (loading: boolean) => void;

  setConnected: (connected: boolean) => void;

  setError: (error: string | null) => void;

  setExecution: (
    execution: ExecutionSummary | null,
  ) => void;

  setSteps: (
    steps: StepResult[],
  ) => void;

  addStep: (
    step: StepResult,
  ) => void;

  addEvent: (
    event: ExecutionEvent,
  ) => void;

  clear: () => void;
}

export const useExecutionStore =
  create<ExecutionState>((set) => ({
    loading: false,

    connected: false,

    error: null,

    execution: null,

    steps: [],

    events: [],

    setLoading: (loading) =>
      set({
        loading,
      }),

    setConnected: (connected) =>
      set({
        connected,
      }),

    setError: (error) =>
      set({
        error,
      }),

    setExecution: (execution) =>
      set({
        execution,
      }),

    setSteps: (steps) =>
      set({
        steps,
      }),

    addStep: (step) =>
      set((state) => ({
        steps: [...state.steps, step],
      })),

    addEvent: (event) =>
      set((state) => ({
        events: [...state.events, event],
      })),

    clear: () =>
      set({
        loading: false,
        connected: false,
        error: null,
        execution: null,
        steps: [],
        events: [],
      }),
  }));