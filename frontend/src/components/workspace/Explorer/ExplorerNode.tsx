import {
  ChevronDown,
  ChevronRight,
  File,
  Folder,
  FolderOpen,
} from "lucide-react";

import {
  useWorkspaceStore,
} from "@/store";

import type {
  WorkspaceItem,
} from "@/services/workspace";

import {
  ExplorerTree,
} from "./ExplorerTree";

interface ExplorerNodeProps {
  item: WorkspaceItem;
}


export function ExplorerNode({
  item,
}: ExplorerNodeProps) {

  const {
    expandedFolders,
    folderChildren,
    loadFolder,
    toggleFolder,
    selectedFile,
    setSelectedFile,
  } = useWorkspaceStore();


  const isDirectory =
    item.type === "directory";


  const expanded =
    expandedFolders.includes(item.path);


  async function handleClick() {

    if (isDirectory) {

      if (!expanded) {
        await loadFolder(item.path);
      }

      toggleFolder(item.path);

      return;
    }

    setSelectedFile(item.path);
  }


  return (
    <div>
      <button
        type="button"
        onClick={handleClick}
        className={`
        flex
        w-full
        items-center
        gap-2
        rounded-lg
        px-2
        py-1.5
        text-left
        text-sm
        transition

        ${selectedFile === item.path
            ? "bg-cyan-500/10 text-cyan-300"
            : "text-white/70 hover:bg-white/5 hover:text-white"
          }
      `}
      >
        {isDirectory && (
          expanded ? (
            <ChevronDown className="h-4 w-4" />
          ) : (
            <ChevronRight className="h-4 w-4" />
          )
        )}

        {isDirectory ? (
          expanded ? (
            <FolderOpen className="h-4 w-4" />
          ) : (
            <Folder className="h-4 w-4" />
          )
        ) : (
          <File className="h-4 w-4" />
        )}

        <span className="truncate">
          {item.name}
        </span>
      </button>

      {isDirectory &&
        expanded &&
        folderChildren[item.path] && (
          <div className="ml-5 mt-1 border-l border-white/10 pl-2">
            <ExplorerTree
              items={
                folderChildren[item.path]
              }
            />
          </div>
        )}
    </div>
  );
}