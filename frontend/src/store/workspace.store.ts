import { create } from "zustand";

import type { PlanStep } from "@/services/planner";

const STORAGE_KEY = "acb-workspace-layout";

type WorkspaceView = "chat" | "workspace" | "planner";

type WorkspacePanel = "chat" | "planner" | "activity";

interface LayoutState {
  activePanel: WorkspacePanel;
  selectedView: WorkspaceView;

  sidebarCollapsed: boolean;
  inspectorCollapsed: boolean;
  bottomPanelCollapsed: boolean;

  sidebarWidth: number;
  inspectorWidth: number;
  bottomPanelHeight: number;
}

interface WorkspaceState {
  /* Existing State */

  selectedFile: string | null;

  currentWorkspace: string | null;

  plan: PlanStep[];

  /* Layout State */

  layout: LayoutState;

  /* Existing Actions */

  setSelectedFile: (file: string | null) => void;

  setWorkspace: (workspace: string | null) => void;

  setPlan: (plan: PlanStep[]) => void;

  clearPlan: () => void;

  /* Layout Actions */

  setActivePanel: (panel: WorkspacePanel) => void;

  setSelectedView: (view: WorkspaceView) => void;

  toggleSidebar: () => void;

  toggleInspector: () => void;

  toggleBottomPanel: () => void;

  setSidebarWidth: (width: number) => void;

  setInspectorWidth: (width: number) => void;

  setBottomPanelHeight: (height: number) => void;
}

function loadLayout(): LayoutState {
  try {
    const value = localStorage.getItem(STORAGE_KEY);

    if (!value) {
      throw new Error();
    }

    return JSON.parse(value);
  } catch {
    return {
      activePanel: "activity",
      selectedView: "workspace",

      sidebarCollapsed: false,
      inspectorCollapsed: false,
      bottomPanelCollapsed: false,

      sidebarWidth: 288,
      inspectorWidth: 320,
      bottomPanelHeight: 320,
    };
  }
}

function saveLayout(layout: LayoutState) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(layout));
}

export const useWorkspaceStore = create<WorkspaceState>((set, get) => ({
  /* Existing */

  selectedFile: null,

  currentWorkspace: null,

  plan: [],

  /* New */

  layout: loadLayout(),

  /* Existing */

  setSelectedFile: (selectedFile) =>
    set({
      selectedFile,
    }),

  setWorkspace: (currentWorkspace) =>
    set({
      currentWorkspace,
    }),

  setPlan: (plan) =>
    set({
      plan,
    }),

  clearPlan: () =>
    set({
      plan: [],
    }),

  /* New */

  setActivePanel: (activePanel) => {
    const layout = {
      ...get().layout,
      activePanel,
    };

    saveLayout(layout);

    set({
      layout,
    });
  },

  setSelectedView: (selectedView) => {
    const layout = {
      ...get().layout,
      selectedView,
    };

    saveLayout(layout);

    set({
      layout,
    });
  },

  toggleSidebar: () => {
    const layout = {
      ...get().layout,
      sidebarCollapsed: !get().layout.sidebarCollapsed,
    };

    saveLayout(layout);

    set({
      layout,
    });
  },

  toggleInspector: () => {
    const layout = {
      ...get().layout,
      inspectorCollapsed: !get().layout.inspectorCollapsed,
    };

    saveLayout(layout);

    set({
      layout,
    });
  },

  toggleBottomPanel: () => {
    const layout = {
      ...get().layout,
      bottomPanelCollapsed: !get().layout.bottomPanelCollapsed,
    };

    saveLayout(layout);

    set({
      layout,
    });
  },

  setSidebarWidth: (sidebarWidth) => {
    const layout = {
      ...get().layout,
      sidebarWidth,
    };

    saveLayout(layout);

    set({ layout });
  },

  setInspectorWidth: (inspectorWidth) => {
    const layout = {
      ...get().layout,
      inspectorWidth,
    };

    saveLayout(layout);

    set({ layout });
  },

  setBottomPanelHeight: (bottomPanelHeight) => {
    const layout = {
      ...get().layout,
      bottomPanelHeight,
    };

    saveLayout(layout);

    set({ layout });
  },
}));
