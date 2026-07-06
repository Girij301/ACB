import { useState } from "react";

import {
  ExecutionService,
  type StepResult,
} from "@/services/execution";

export function useExecution() {
  const [steps, setSteps] = useState<
    StepResult[]
  >([]);

  const [loading, setLoading] =
    useState(false);

  async function execute(
    sessionId: string,
    task: string,
  ) {
    setLoading(true);

    try {
      const response =
        await ExecutionService.execute({
          session_id: sessionId,
          task,
        });

      setSteps(response.steps);
    } finally {
      setLoading(false);
    }
  }

  return {
    steps,
    loading,
    execute,
  };
}