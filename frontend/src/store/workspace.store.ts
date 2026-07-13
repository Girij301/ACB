import { create } from "zustand";

interface WorkspaceState {
  selectedFile: string | null;

  currentWorkspace: string | null;

  setSelectedFile: (
    file: string | null,
  ) => void;

  setWorkspace: (
    workspace: string | null,
  ) => void;
}

export const useWorkspaceStore =
  create<WorkspaceState>((set) => ({
    selectedFile: null,

    currentWorkspace: null,

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
  }));