import { useState } from "react";

import {
  ExecutionService,
  type StepResult,
  type ExecutionSummary,
} from "@/services/execution";

export function useExecution() {
  const [steps, setSteps] = useState<StepResult[]>([]);

  const [execution, setExecution] =
    useState<ExecutionSummary | null>(null);

  const [loading, setLoading] = useState(false);

  const [error, setError] =
    useState<string | null>(null);

  async function execute(
    sessionId: string,
    task: string,
  ) {
    if (loading) return;

    setLoading(true);
    setError(null);

    try {
      const response =
        await ExecutionService.execute({
          session_id: sessionId,
          task,
        });

      setSteps(response.steps);

      setExecution(response.execution);
    } catch (err) {
      console.error("Execution Error:", err);

      setError(
        "Failed to execute the plan. Please try again.",
      );

      setExecution(null);
    } finally {
      setLoading(false);
    }
  }

  return {
    steps,
    execution,
    loading,
    error,
    execute,
  };
}