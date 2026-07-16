import {
  FolderOpen,
  RefreshCw,
  Search,
} from "lucide-react";

import { useMemo } from "react";

import {
  useWorkspaceStore,
} from "@/store";

import {
  explorerVariants,
} from "./explorerVariants";

import {
  ExplorerTree,
} from "./ExplorerTree";


export function Explorer() {

  const {
    explorerTree,
    explorerLoading,
    explorerRefreshing,
    explorerSearchQuery,
    setExplorerSearchQuery,
    refreshExplorer,
  } = useWorkspaceStore();

  const filteredTree = useMemo(() => {
    const query =
      explorerSearchQuery.trim().toLowerCase();

    if (!query) {
      return explorerTree;
    }

    return explorerTree.filter((item) =>
      item.name.toLowerCase().includes(query),
    );
  }, [explorerTree, explorerSearchQuery]);

  return (
    <section
      className={explorerVariants()}
    >

      <div
        className="
        flex
        items-center
        justify-between
        border-b
        border-white/10
        px-4
        py-3
      "
      >
        <div className="flex items-center gap-2">
          <FolderOpen
            className="h-4 w-4 text-cyan-300"
          />

          <h3
            className="
            text-sm
            font-semibold
            text-white
          "
          >
            Explorer
          </h3>
        </div>

        <button
          type="button"
          onClick={refreshExplorer}
          disabled={explorerRefreshing}
          className="
            rounded-lg
            p-1.5
            text-white/60
            transition
            hover:bg-white/10
            hover:text-white
            disabled:opacity-40
          "
          title="Refresh Explorer"
        >
          <RefreshCw
            className={`
              h-4 w-4
              ${explorerRefreshing
                ? "animate-spin"
                : ""
              }
            `}
          />
        </button>
      </div>
      

      <div
        className="
          min-h-0
          flex-1
          overflow-auto
          p-3
        "
      >

        <div className="relative mb-3">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-white/40" />

          <input
            type="text"
            value={explorerSearchQuery}
            onChange={(e) =>
              setExplorerSearchQuery(e.target.value)
            }
            placeholder="Search files..."
            className="
            w-full
            rounded-lg
            border
            border-white/10
            bg-white/5
            py-2
            pl-9
            pr-3
            text-sm
            text-white
            outline-none
            placeholder:text-white/40
            focus:border-cyan-500/40
          "
          />
        </div>

        {explorerLoading && (
          <p className="text-sm text-white/50">
            Loading workspace...
          </p>
        )}


        {!explorerLoading &&
          filteredTree.length === 0 && (
            <p className="text-sm text-white/50">
              {explorerSearchQuery
                ? "No matching files"
                : "Empty workspace"}
            </p>
          )}


        {!explorerLoading &&
          explorerTree.length > 0 && (
            <ExplorerTree
              items={filteredTree}
            />
          )}

      </div>

    </section>
  );
}