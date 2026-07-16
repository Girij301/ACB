import { create } from "zustand";

import type { PlanStep } from "@/services/planner";
import { WorkspaceService } from "@/services/workspace";

const STORAGE_KEY = "acb-workspace-layout";

type WorkspaceView = "chat" | "workspace" | "planner";

type WorkspacePanel = "chat" | "planner" | "activity";

export interface ExplorerItem {
  name: string;
  type: "directory" | "file";
  path: string;
}

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

  fileContent: string | null;

  currentWorkspace: string | null;

  plan: PlanStep[];

  explorerTree: ExplorerItem[];

  folderChildren: Record<string, ExplorerItem[]>;

  loadedFolders: string[];

  expandedFolders: string[];

  explorerLoading: boolean;

  explorerRefreshing: boolean;

  explorerSearchQuery: string;

  explorerAutoRefresh: boolean;

  /* Layout State */

  layout: LayoutState;

  /* Existing Actions */

  setSelectedFile: (file: string | null) => void;

  setFileContent: (content: string | null) => void;

  setWorkspace: (workspace: string | null) => void;

  setPlan: (plan: PlanStep[]) => void;

  clearPlan: () => void;

  /*workspace action */

  setExplorerTree: (tree: ExplorerItem[]) => void;

  setFolderChildren: (folder: string, children: ExplorerItem[]) => void;

  markFolderLoaded: (folder: string) => void;

  loadFolder: (folder: string) => Promise<void>;

  refreshExplorer: () => Promise<void>;

  toggleFolder: (path: string) => void;

  setExplorerLoading: (loading: boolean) => void;

  setExplorerRefreshing: (refreshing: boolean) => void;

  setExplorerSearchQuery: (query: string) => void;

  setExplorerAutoRefresh: (enabled: boolean) => void;

  resetExplorer: () => void;

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

  fileContent: null,

  currentWorkspace: null,

  plan: [],

  explorerTree: [],

  folderChildren: {},

  loadedFolders: [],

  expandedFolders: [],

  explorerLoading: false,

  explorerRefreshing: false,

  explorerSearchQuery: "",

  explorerAutoRefresh: true,

  /* New */

  layout: loadLayout(),

  /* Existing */

  setSelectedFile: (selectedFile) =>
    set({
      selectedFile,
    }),

  setFileContent: (fileContent) =>
    set({
      fileContent,
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

  setExplorerTree: (explorerTree) =>
    set({
      explorerTree,
    }),

  setFolderChildren: (folder, children) =>
    set((state) => ({
      folderChildren: {
        ...state.folderChildren,
        [folder]: children,
      },
    })),

  markFolderLoaded: (folder) =>
    set((state) => ({
      loadedFolders: [...state.loadedFolders, folder],
    })),

  loadFolder: async (folder) => {
    const state = get();

    if (state.loadedFolders.includes(folder)) {
      return;
    }

    try {
      const response = await WorkspaceService.listDirectory({
        path: folder,
      });

      get().setFolderChildren(folder, response.data.items);

      get().markFolderLoaded(folder);
    } catch (error) {
      console.error("Failed loading folder:", error);
    }
  },

  refreshExplorer: async () => {
    set({
      explorerRefreshing: true,
    });

    try {
      const response = await WorkspaceService.listDirectory();

      set({
        explorerTree: response.data.items,
      });
    } catch (error) {
      console.error("Explorer refresh failed:", error);
    } finally {
      set({
        explorerRefreshing: false,
      });
    }
  },

  toggleFolder: (path) =>
    set((state) => ({
      expandedFolders: state.expandedFolders.includes(path)
        ? state.expandedFolders.filter((folder) => folder !== path)
        : [...state.expandedFolders, path],
    })),

  setExplorerLoading: (explorerLoading) =>
    set({
      explorerLoading,
    }),

  setExplorerRefreshing: (explorerRefreshing) =>
    set({
      explorerRefreshing,
    }),

  setExplorerSearchQuery: (explorerSearchQuery) =>
    set({
      explorerSearchQuery,
    }),

  setExplorerAutoRefresh: (explorerAutoRefresh) =>
    set({
      explorerAutoRefresh,
    }),

  resetExplorer: () =>
    set({
      explorerTree: [],
      folderChildren: {},
      loadedFolders: [],
      expandedFolders: [],
      explorerLoading: false,
      explorerRefreshing: false,
      explorerSearchQuery: "",
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
