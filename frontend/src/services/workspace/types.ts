export type WorkspaceItemType =
  | "file"
  | "directory";


export interface WorkspaceItem {
  name: string;

  type: WorkspaceItemType;

  path: string;
}


export interface ListDirectoryRequest {
  path?: string;
}


export interface WorkspaceResponse<T> {
  success: boolean;

  message: string;

  data: T;
}


export interface ListDirectoryResponse {
  items: WorkspaceItem[];
}


export interface ReadFileResponse {
  content: string;
}