import { useState } from "react";

import {
  PlannerService,
  type PlanStep,
} from "@/services/planner";

export function usePlanner() {
  const [plan, setPlan] = useState<PlanStep[]>([]);
  const [loading, setLoading] = useState(false);

  async function createPlan(
    sessionId: string,
    task: string,
  ) {
    setLoading(true);

    try {
      const response =
        await PlannerService.createPlan({
          session_id: sessionId,
          task,
        });

      console.group("Planner Response");
      console.log("Full Response:", response);
      console.log("Plan Length:", response.data.plan.length);
      console.table(response.data.plan);
      console.groupEnd();

      setPlan(response.data.plan);
    } catch (error) {
      console.error("Planner Error:", error);

      setPlan([]);
    } finally {
      setLoading(false);
    }
  }

  return {
    plan,
    loading,
    createPlan,
  };
}