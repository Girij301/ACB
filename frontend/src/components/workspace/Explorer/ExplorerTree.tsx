import type {
  WorkspaceItem,
} from "@/services/workspace";

import {
  ExplorerNode,
} from "./ExplorerNode";


interface ExplorerTreeProps {
  items: WorkspaceItem[];
}


export function ExplorerTree({
  items,
}: ExplorerTreeProps) {

  return (
    <div className="space-y-1">
      {items.map((item) => (
        <ExplorerNode
          key={item.path}
          item={item}
        />
      ))}
    </div>
  );
}