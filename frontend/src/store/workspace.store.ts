import { create } from "zustand";

import type { PlanStep } from "@/services/planner";


interface WorkspaceState {

  selectedFile: string | null;

  currentWorkspace: string | null;


  plan: PlanStep[];


  setSelectedFile: (
    file: string | null,
  ) => void;


  setWorkspace: (
    workspace: string | null,
  ) => void;


  setPlan: (
    plan: PlanStep[],
  ) => void;


  clearPlan: () => void;

}



export const useWorkspaceStore =
  create<WorkspaceState>((set) => ({

    selectedFile: null,


    currentWorkspace: null,


    plan: [],



    setSelectedFile: (
      selectedFile,
    ) =>
      set({
        selectedFile,
      }),



    setWorkspace: (
      currentWorkspace,
    ) =>
      set({
        currentWorkspace,
      }),



    setPlan: (
      plan,
    ) =>
      set({
        plan,
      }),



    clearPlan: () =>
      set({
        plan: [],
      }),

  }));